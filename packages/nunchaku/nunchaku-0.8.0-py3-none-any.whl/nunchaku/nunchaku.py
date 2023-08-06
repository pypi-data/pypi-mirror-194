from ._models import mc, mc_t, mc_entropy
import numpy as np
from scipy.optimize import minimize
from scipy.stats import linregress
import matplotlib.pyplot as plt
from logging import warning
from ._example_data import return_data
import pandas as pd


class Nunchaku:
    """Find how many linear regions a dataset should be divide into,
    and find the start and end of each linear region.

    Parameters
    ----------
    X : list of floats or 1-D numpy array
        the x vector of data.
    Y : array-like
        the y vector or matrix of data, each row being one replicate of
        measurement.
    prior : list of length 2 or 4
        the prior range of the slope (and the intercept when length is 4).
    std : list of floats or 1-D numpy array, optional # error?
        the standard deviation of the input data.
    start : int, default 0
        the min index of x that a valid region allows.
    end : int, optional
        the max index of x that a valid region allows (inclusive).
    estimate_std : bool, optional
        if True, estimate std from data; default True when Y has >= 3
        replicates.
    minlen : int, default 3
        the minimal length of a valid region (must be >= 3).
    attempt : int, default 20
        the max number of attempts to run the BFGS minimize routine when the std
        is neither provided nor estimated.

    Raises
    ------
    ValueError
        when Y has multiple replicates and std is provided.

    Examples
    --------
    >>> from nunchaku.nunchaku import nunchaku, get_example_data
    >>> x, y = get_example_data()
    >>> nc = nunchaku(x, y, prior=[-5,5]) # load data and set prior of slope
    >>> # compare models with one, two or three linear regions
    >>> num_regions, evidences = nc.get_number([1,2,3])
    >>> # get the mean and standard deviation of the boundary points
    >>> bds, bds_std = nc.get_iboundaries(num_regions)
    >>> info_df = nc.get_info()
    >>> nc.plot(info_df)

    """

    def __init__(
        self,
        X,
        Y,
        prior,
        std=None,
        start=0,
        end=None,
        estimate_std="default",
        minlen=3,
        attempt=20,
    ):
        # Load settings
        self.X = np.asarray(X)
        self.Y = np.asarray(Y)
        if isinstance(std, (list, np.ndarray)):
            self.std = np.asarray(std)
        else:
            self.std = None
        self.start = start
        if end:
            self.end = end
        else:
            self.end = self.X.shape[0]
        if minlen >= 3:
            self.minlen = minlen
        else:
            warning("Nunchaku: minlen must be >= 3. Reset to 3.")
            self.minlen = 3
        self.attempt = attempt
        # handle estimate_std
        if estimate_std == "default":
            # if Y has 3 replicates and std is none
            if (self.Y.ndim > 1) and (self.Y.shape[0] >= 3) and (self.std is None):
                estimate_std = True
            else:
                estimate_std = False
        # if std is provided, do not estimate_std (overwrite user's setting)
        if self.std is not None:
            estimate_std = False
        # if std is not provided but Y is 1-D, impossible to estimate_std
        elif self.Y.ndim == 1:
            estimate_std = False
        # if std is provided but Y is 2-D, throw error
        if self.std is not None and self.Y.ndim > 1:
            raise ValueError("When std is provided, Y should be 1-D.")
        # now estimate std
        self.estimate_std = estimate_std
        if estimate_std:
            # x, y, instead of X, Y, are what the methods actually use
            self.x = self.X
            self.y = self.Y.mean(axis=0)
            # OK to write std because estimate_std is True only when std is None
            self.std = self.Y.std(axis=0)
        else:
            self.x = self.X
            self.y = self.Y
        # handle estimated std=0 when replicates have the same value by chance
        if self.std is not None:
            self.std[self.std == 0] = self.std[self.std > 0].mean()
        # prior
        if prior:
            if len(prior) == 2:
                prior.append(-self.x[-1] * prior[1])
                prior.append(-self.x[-1] * prior[0])
            elif len(prior) != 4:
                raise ValueError(f"len(prior) should be 2 or 4, not {prior}.")
            self.prior = prior
            self.logpmc = -np.log((prior[1] - prior[0]) * (prior[3] - prior[2]))
        else:
            self.logpmc = None
        # results
        self.evidence = self._cal_evidence()

    def _cal_evidence(self):
        """Calculate evidence for each possible region between start and end."""
        X, Y, std, start, end, minlen = (
            self.x,
            self.y,
            self.std,
            self.start,
            self.end,
            self.minlen,
        )
        # Matrix to record results
        results = np.ones((len(X), len(X))) * np.nan
        results.fill(np.nan)
        if self.std is None:
            init_guess = self._get_init_guess()
            funcs = mc_t()
        else:
            logL = mc()
        # calculate evidence
        if self.std is None:
            warning("Nunchaku: Std is not estimated or provided. It could be slow.")
            for st in range(start, end - minlen + 1):
                for ed in range(st + minlen, end + 1):  # confirm?
                    # Run calculation and update init_guess
                    init_guess, evi = self._cal_evidence_unknown_s(
                        st, ed, init_guess, funcs
                    )
                    if evi is None:
                        continue
                    else:
                        results[st, ed - 1] = evi
        else:
            for st in range(start, end - minlen + 1):
                for ed in range(st + minlen, end + 1):  # confirm?
                    evi = logL(X[st:ed], Y[st:ed], std[st:ed], ed - st)
                    # unknown bug in either builtin sum or numpy sum
                    if evi > 9e8:
                        evi = -np.inf
                    results[st, ed - 1] = evi  # must be (end - 1)?
        # Normalise to start:end
        # self.norm_factor = results[start, end - 1]
        # results = results - results[start, end - 1]
        return results

    def get_number(self, num_regions):
        """Get the most likely number of linear regions.

        Parameters
        ----------
        num_regions : list of int
            number of linear regions

        """
        res = self.evidence.copy()
        res = res.astype(np.longdouble)
        # normalise to avoid overflow
        log_norm_factor = np.nanmax(res)
        res = np.exp(res - np.nanmax(res))
        res[np.isnan(res)] = 0
        evi = []
        for M in num_regions:
            with np.errstate(divide="ignore", invalid="ignore"):
                evi_M = (
                    np.log(self._findZ(res, M))
                    + self._mc_logprior(M)
                    + self.logpmc * M
                    + log_norm_factor * M
                ) / np.log(10)
            evi.append(evi_M)
        ind = np.nanargmax(evi)
        best_num_regions = num_regions[ind]
        return best_num_regions, evi

    def get_info(self, boundaries):
        """Return a Pandas dataframe that describes the regions within given internal boundaries,
        i.e. excluding the first (0) and last (`len(x)`) indices of the data.

        Parameters
        ----------
        boundaries : list of int
            a list of indices of boundary points

        """
        all_matrix, x, y = (self.evidence, self.x, self.y)
        keys = [
            "start",
            "end",
            "evidence",
            "slope",
            "intercept",
            "rsquare",
            "x range",
            "y range",
            "entropy",
        ]
        d = {k: [] for k in keys}
        d["start"] = [0] + list(map(lambda x: x + 1, boundaries))
        d["end"] = boundaries + [len(self.x) - 1]
        for st, ed in zip(d["start"], d["end"]):
            d["evidence"].append(all_matrix[st, ed])
            if y.ndim > 1:
                # flatten for regression
                x_flat = np.append([], [x[st : ed + 1]] * y.shape[0])
                y_flat = y[:, st : ed + 1].flatten(order="C")
                y_mn = y[:, st : ed + 1].mean(axis=0)
            else:
                x_flat = x[st : ed + 1]
                y_flat = y[st : ed + 1]
                y_mn = y[st : ed + 1]
            d["x range"].append((x_flat[0], x_flat[-1]))
            d["y range"].append((y_mn[0], y_mn[-1]))
            lin_res = linregress(x_flat, y_flat)
            d["slope"].append(lin_res.slope)
            d["intercept"].append(lin_res.intercept)
            d["rsquare"].append(lin_res.rvalue**2)
            if self.std is not None:
                d["entropy"].append(self._get_entropy(st, ed))  # no need to ed+1
            else:
                d["entropy"].append(np.nan)
        return pd.DataFrame(d)

    def get_iboundaries(self, num_regions, round=True):
        """Return the mean and standard deviation of the internal boundary indices,
        i.e. excluding the first (0) and last (`len(x)`) indices of the data.

        Parameters
        ----------
        num_regions : int
            number of linear regions
        round : bool
            whether to round the returned mean to integer

        """
        res = self.evidence.copy()
        res = res.astype(np.longdouble)
        # normalise to avod overflow
        # log_norm_factor = np.nanmax(res)
        res = np.exp(res - np.nanmax(res))
        res[np.isnan(res)] = 0
        Z = self._findZ(res, num_regions)
        boundaries = []
        boundaries_std = []
        for j in range(1, num_regions):
            coo = self._find_moment(res, num_regions, j) / Z
            boundaries.append(coo)
            coo2 = self._find_moment(res, num_regions, j, moment=2) / Z
            boundaries_std.append(np.sqrt(coo2 - coo**2))
        if round:
            return list(np.array(boundaries).astype(int)), boundaries_std
        else:
            return boundaries, boundaries_std

    def plot(
        self,
        info_df=None,
        show=False,
        figsize=(6, 5),
        std_width=1,
        s=10,
        color="red",
        alpha=0.5,
        **kwargs,
    ):
        """Plot the raw data and the boundary points.

        Parameters
        ----------
        info_df : pandas dataframe, default None
            the pandas dataframe returned by `get_info()`; if None, only the data is shown.
        show : bool
            if True, call `plt.show()`
        figsize : tuple
            size of figure passed to `plt.subplots()`
        std_width : float
            the width of the error bar is this parameter times std times 2 (both
            sides)
        s : float
            size of the boundary points as passed into `plt.scatter()`
        color : str
            color of the boundary points as passed into `plt.scatter()`
        alpha : float
            transparency of the boundary points as passed into `plt.scatter()`
        **kwargs : keyword arguments
            as passed into `plt.plot()`

        Examples
        --------
        `plot()` returns both the figure and axes, enabling users to customise them

        >>> from nunchaku.nunchaku import nunchaku
        >>> nc = nunchaku(x, y)
        >>> bds, _ = nc.get_iboundaries(3)
        >>> info_df = nc.get_info(bds)
        >>> fig, ax = nc.plot(info_df)

        """

        if self.y.ndim > 1:
            y = self.y.mean(axis=0)
            std = None
        else:
            y = self.y
            std = self.std
        fig, ax = plt.subplots(figsize=figsize)
        ax.plot(self.x, y, color="blue")
        if std is not None:
            ax.fill_between(
                self.x,
                y - std_width * std,
                y + std_width * std,
                alpha=0.1,
                color="blue",
            )
        if info_df is not None:
            for j in range(info_df.shape[0]):
                bd_start = info_df.loc[j, "start"]
                bd_end = info_df.loc[j, "end"]
                slope = info_df.loc[j, "slope"]
                intercept = info_df.loc[j, "intercept"]
                y_start = slope * self.x[bd_start] + intercept
                y_end = slope * self.x[bd_end] + intercept
                ax.plot(
                    [self.x[bd_start], self.x[bd_end]],
                    [y_start, y_end],
                    color=color,
                    alpha=alpha,
                    marker="o",
                    markersize=s,
                    **kwargs,
                )
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        if show:
            plt.show()
        return fig, ax

    def plot_matrix(self, show=False, figsize=(6, 5), **kwargs):
        """Plot the evidence for all calcuated segments.

        Parameters
        ----------
        show : bool
            if True, call `plt.show()`

        figsize : tuple, default (6, 5)
            figsize passed on to `matplotlib.pyplot.figure`.

        kwargs :
            keyword arguments to be passed to `matplotlib.axes.Axes.plot`
            when result="from", otherwise `matplotlib.axes.Axes.imshow`.

        Examples
        --------
        `plot_matrix()` returns both the figure and axes, enabling users to customise them

        >>> from nunchaku.nunchaku import nunchaku
        >>> nc = nunchaku(x, y)
        >>> fig, ax = nc.plot_matrix()
        >>> ax.set_ylim(200,)

        """
        res = self.evidence
        fig = plt.figure(constrained_layout=True, figsize=figsize)
        # create three axes
        gs = fig.add_gridspec(
            2,
            2,
            width_ratios=(4, 1),
            height_ratios=(1, 4),
        )
        ax = fig.add_subplot(gs[1, 0])
        ax_mgx = fig.add_subplot(gs[0, 0], sharex=ax)
        ax_mgy = fig.add_subplot(gs[1, 1], sharey=ax)
        # calculate marginal
        res_norm = np.exp(res - np.nanmax(res))
        with np.errstate(invalid="ignore"):  # ignore the zero division case
            mgx = np.nansum(res_norm, axis=0) / np.sum(~np.isnan(res_norm), axis=0)
            mgy = np.nansum(res_norm, axis=1) / np.sum(~np.isnan(res_norm), axis=1)
        img = ax.imshow(res, origin="lower", aspect="auto", **kwargs)
        fig.colorbar(img, ax=ax, location="left", use_gridspec=True)
        ax.set_ylabel("index of start")
        ax.set_xlabel("index of end")
        ax_mgx.plot(mgx)
        ax_mgx.xaxis.set_tick_params(labelbottom=False)
        ax_mgy.plot(mgy, range(len(mgy)))
        ax_mgy.yaxis.set_tick_params(labelleft=False)
        axes = [ax, ax_mgx, ax_mgy]
        if show:
            plt.show()
        return fig, axes

    ### Internal functions for single region
    ###

    def _find_from_unknown_s(self):
        """calculate the evidence when the std is unknown.

        Raises
        ------
        ValueError
            when the length of longest region is smaller than the minlen.

        """

        res = []
        start, end, minlen = (
            self.start,
            self.end,
            self.minlen,
        )
        funcs = mc_t()
        if end - start <= minlen:
            raise ValueError(f"(end - start) must be no less than {minlen}.")
        # Initial guess with linear regression
        init_guess = self._get_init_guess()
        # Go through N's
        for n in range(minlen, end + 1 - start):
            # Run calculation and update init_guess
            init_guess, evi = self._cal_evidence_unknown_s(
                start, start + n, init_guess, funcs
            )
            if evi is None:
                break
            else:
                res.append(evi)
        return res

    def _get_init_guess(self):
        """get initial guess by regressing over the whole x and y"""
        X, Y = self.x, self.y
        if Y.ndim > 1:
            # take the first rep as first guess
            lin_res = linregress(X, Y[0, :])
        else:
            lin_res = linregress(X, Y)
        init_guess = (lin_res.slope, lin_res.intercept)
        return init_guess

    def _cal_evidence_unknown_s(self, start, end, init_guess, funcs):
        """calculate evidence without std

        Parameters
        ----------
        start : init
            start of region
        end : int
            end of region (inclusive)
        init_guess : tuple
            initial guess for scipy.optimize.minimize
        funcs : tuple of functions
            tuple of -logL, hessian and jacobian.

        """
        X, Y, attempt = (
            self.x,
            self.y,
            self.attempt,
        )
        neglogL, hess, jac = funcs
        # flatten multiple reps
        if Y.ndim > 1:
            X_flat = np.append([], [X[start:end]] * Y.shape[0])  # flatten X
            Y_flat = Y[:, start:end].flatten(order="C")
            n_flat = len(X[start:end]) * Y.shape[0]
        else:
            X_flat = X[start:end]
            Y_flat = Y[start:end]
            n_flat = len(X[start:end])
        # run multiple attempts in case optimisation fails
        for k in range(attempt):
            # Guess m and c
            th00 = np.random.normal(init_guess[0], 2 * np.abs(init_guess[0]))
            th01 = np.random.normal(init_guess[1], 2 * np.abs(init_guess[1]))
            th0 = (th00, th01)
            # Find optimum
            with np.errstate(invalid="raise", divide="raise"):
                try:
                    th_opt = minimize(
                        neglogL,
                        th0,
                        (X_flat, Y_flat, n_flat),
                        method="BFGS",
                        jac=jac,
                    )
                except FloatingPointError:
                    continue
            if th_opt.success:
                init_guess = th_opt.x  # Update guess
                hess_opt = hess(th_opt.x, X_flat, Y_flat, n_flat)
                maxL = -th_opt.fun
                det = np.linalg.det(hess_opt / (2 * np.pi))
                if det > 0:
                    invdetsqrt = -np.log(det) / 2
                    return (init_guess, maxL + invdetsqrt)
                else:
                    continue
        else:
            # After running all attempts, still not return, then None
            return (None, None)

    ### Internal functions for model comparison and exact posterior
    ###

    def _mc_logprior(self, num_regions):
        """return the log value of the uniform prior given number of boundary points"""
        res = self.evidence.copy()
        res[~np.isnan(res)] = 1
        res[np.isnan(res)] = 0
        return -np.log(self._findZ(res, num_regions))

    def _findZ(self, exp_res, number, vec=None):
        """finding the normalising factor of the posterior"""
        datalen = len(self.x)
        if vec is None:
            if number == 1:
                return exp_res[0, -1]
            else:
                f_M = list(exp_res[:, datalen - 1])
                f_M = np.array([f_M[1:] + [0]])
                return self._findZ(exp_res, number - 1, f_M)
        else:
            if number == 1:
                return np.matmul(exp_res[0, :], vec.T)[0]
            else:
                f_M = []
                for n in range(datalen):
                    f_M.append(np.matmul(exp_res[n, :], vec.T)[0])
                f_M = np.array([f_M[1:] + [0]])
                return self._findZ(exp_res, number - 1, f_M)

    def _find_moment(self, exp_res, number, k, moment=1, vec=None):
        """finding the moments of the posterior"""
        datalen = len(self.x)
        if vec is None:
            if number == 1:
                return None
            else:  # k < number when vec is None
                f_M = list(exp_res[:, datalen - 1])
                f_M = np.array([f_M[1:] + [0]])
                return self._find_moment(exp_res, number - 1, k, moment, f_M)
        else:
            if number == 1:
                if k == number:
                    return np.matmul(
                        exp_res[0, :],
                        vec.T * np.arange(datalen).reshape(datalen, 1) ** moment,
                    )[0]
                else:
                    return np.matmul(exp_res[0, :], vec.T)[0]
            else:
                f_M = []
                if k == number:
                    for n in range(datalen):
                        f_M.append(
                            np.matmul(
                                exp_res[n, :],
                                vec.T
                                * np.arange(datalen).reshape(datalen, 1) ** moment,
                            )[0]
                        )
                    f_M = np.array([f_M[1:] + [0]])
                    return self._find_moment(exp_res, number - 1, k, moment, f_M)
                else:
                    for n in range(datalen):
                        f_M.append(np.matmul(exp_res[n, :], vec.T)[0])
                    f_M = np.array([f_M[1:] + [0]])
                    return self._find_moment(exp_res, number - 1, k, moment, f_M)

    ### getting entropy
    ###
    def _get_entropy(self, start, end):
        # end is inclusive
        x = self.x[start : end + 1]
        y = self.y[start : end + 1]
        std = self.std[start : end + 1]
        N = len(x)
        logevi = self.evidence[start, end]
        func = mc_entropy()
        return func(x, y, std, N, logevi)


def get_example_data(plot=False):
    """Return example data, with x being cell number and y being three replicates of OD measurement.

    Parameters
    ----------
    plot : bool, default False
        If true, plot the example data.

    Examples
    --------
    >>> from nunchaku.nunchaku import get_example_data
    >>> x, y = get_example_data()
    """
    x, y = return_data()
    if plot:
        fig, ax = plt.subplots()
        for j in range(y.shape[0]):
            ax.scatter(x, y[j, :], alpha=0.7, color="b")
        ax.set_xlabel("cell number")
        ax.set_ylabel("optical density (OD)")
        plt.plot()
    return x, y
