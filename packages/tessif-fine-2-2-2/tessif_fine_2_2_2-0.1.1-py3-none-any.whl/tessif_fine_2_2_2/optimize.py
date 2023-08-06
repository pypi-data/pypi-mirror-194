"""Wrapping the fine optimization process."""

from tessif.frused.utils import HideStdoutPrinting


def optimize(system_model, solver="cbc", tsa=False, **kwargs):
    """Optimize an energy system using `fine
    <https://vsa-fine.readthedocs.io/en/latest/index.html>`_ .

    Parameters
    ----------
    system_model: fine energy system model
        fine energy system to be simulated

    solver: str, default='cbc'
        String specifying the solver to be used. For `FOSS
        <https://en.wikipedia.org/wiki/Free_and_open-source_software>`_
        application, this is usually either ``cbc`` or ``glpk``.

        But since :mod:`pyomo` is used for interfacing the solver. Any of it's
        `supported solvers
        <https://pyomo.readthedocs.io/en/stable/solving_pyomo_models.html#supported-solvers>`_
        can be used.

        Note
        ----
        In case the link above is servered, use the pyomo command::

            pyomo help --solvers

    kwargs:
        Keywords parameterizing the solver used as well as the energy system
        transformation process.


    Return
    ------
    optimized fine system model
        Energy system carrying the optimization results.
    """

    kwargs["solver"] = solver

    # Parse time series aggregatin
    # False - the full time series
    # True - clustered time series data.
    if tsa is True:
        kwargs["timeSeriesAggregation"] = True
        system_model.cluster()
    else:
        kwargs["timeSeriesAggregation"] = False

    # supress solver results getting printed to stdout
    with HideStdoutPrinting():
        system_model.optimize(**kwargs)

    return system_model
