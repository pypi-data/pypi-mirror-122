# Author: Nicolas Legrand <nicolas.legrand@cfin.au.dk>

from typing import Dict, List, Tuple, Union, overload

import numpy as np
from bokeh.plotting.figure import Figure
from matplotlib.axes import Axes

from systole.correction import rr_artefacts
from systole.plots.utils import get_plotting_function
from systole.utils import input_conversion


@overload
def plot_subspaces(
    rr: None, artefacts: Dict[str, np.ndarray], input_type: str = "rr_ms"
) -> Union[Figure, Axes]:
    ...


@overload
def plot_subspaces(
    rr: Union[List[float], np.ndarray], artefacts: None, input_type: str = "rr_ms"
) -> Union[Figure, Axes]:
    ...


@overload
def plot_subspaces(
    rr: Union[List[float], np.ndarray],
    artefacts: Dict[str, np.ndarray],
    input_type: str = "rr_ms",
) -> Union[Figure, Axes]:
    ...


def plot_subspaces(
    rr=None,
    artefacts=None,
    input_type: str = "rr_s",
    figsize: Union[Tuple[float, float], int] = None,
    backend: str = "matplotlib",
) -> Union[Figure, Axes]:
    """Visualization of short, long, extra, missed and ectopic beats detection.

    The artefact detection is based on the method described in [1]_.

    Parameters
    ----------
    rr : :py:class:`numpy.ndarray` | None
        Interval time-series (R-R, beat-to-beat...), in seconds or in
        miliseconds.
    artefacts : dict | None
        The artefacts detected using
        :py:func:`systole.detection.rr_artefacts()`.
    input_type : str
        The type of input vector. Default is `"peaks"` (a boolean vector where
        `1` represents the occurrence of R waves or systolic peaks).
        Can also be `"rr_s"` or `"rr_ms"` for vectors of RR intervals, or
        interbeat intervals (IBI), expressed in seconds or milliseconds
        (respectively).
    backend: str
        Select plotting backend {"matplotlib", "bokeh"}. Defaults to
        "matplotlib".
    figsize : tuple | int | None
        Figure size. Default is `(12, 6)` for matplotlib backend, and the
        height is `600` when using bokeh backend.

    Returns
    -------
    plot : :class:`matplotlib.axes.Axes` or :class:`bokeh.plotting.figure.Figure`
        The matplotlib axes, or the boken figure containing the plot.

    See also
    --------
    plot_events, plot_ectopic, plot_shortlong, plot_subspaces, plot_frequency,
    plot_timedomain, plot_nonlinear

    References
    ----------
    .. [1] Lipponen, J. A., & Tarvainen, M. P. (2019). A robust algorithm for
       heart rate variability time series artefact correction using novel beat
       classification. Journal of Medical Engineering & Technology, 43(3),
       173–181. https://doi.org/10.1080/03091902.2019.1640306

    Notes
    -----
    If both `rr` and `artefacts` are provided, the function will drop `artefacts`
    and re-evaluate given the current RR time-series.

    Examples
    --------

    Visualizing artefacts from RR time series.

    .. jupyter-execute::

       from systole import import_rr
       from systole.plots import plot_subspaces

       # Import PPG recording as numpy array
       rr = import_rr().rr.to_numpy()
       plot_subspaces(rr, backend="bokeh")

    Visualizing ectopic subspace from the `artefact` dictionary.

    .. jupyter-execute::

       from systole.detection import rr_artefacts

       # Use the rr_artefacts function to short/long and extra/missed intervals
       artefacts = rr_artefacts(rr)

       plot_subspaces(artefacts=artefacts)

    Using the Bokeh backend.

    .. jupyter-execute::

       from bokeh.io import output_notebook
       from bokeh.plotting import show
       from systole.detection import rr_artefacts
       output_notebook()

       show(
          plot_subspaces(artefacts=artefacts, backend="bokeh")
       )

    """
    if figsize is None:
        if backend == "matplotlib":
            figsize = (12, 6)
        elif backend == "bokeh":
            figsize = 600

    if artefacts is None:
        if rr is None:
            raise ValueError("rr or artefacts should be provided")
        else:
            if input_type != "rr_ms":
                rr = input_conversion(rr, input_type=input_type, output_type="rr_ms")
            artefacts = rr_artefacts(rr)

    plot_subspaces_args = {
        "artefacts": artefacts,
        "figsize": figsize,
    }

    plotting_function = get_plotting_function(
        "plot_subspaces", "plot_subspaces", backend
    )
    plot = plotting_function(**plot_subspaces_args)

    return plot
