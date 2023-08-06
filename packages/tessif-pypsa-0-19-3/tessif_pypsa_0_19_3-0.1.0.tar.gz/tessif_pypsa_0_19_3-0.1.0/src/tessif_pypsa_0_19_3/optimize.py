"""Wrapping the pypsa optimization process."""
from tessif.frused.utils import HideStdoutPrinting


def optimize(system_model, solver="cbc", **kwargs):
    """Optimize a PyPSA system model.

    Parameters
    ----------
    system_model: pypsa.Network
        Pypsa energy system to be simulated

    solver: str, default='cbc'
        String specifying the solver to be used. For `FOSS
        <https://en.wikipedia.org/wiki/Free_and_open-source_software>`_
        application, this is usually either ``cbc`` or ``glpk``.

        But since :mod:`pyomo` is used for interfacing the solver. Any of it's
        `supported solvers
        <https://pyomo.readthedocs.io/en/stable/solving_pyomo_models.html#supported-solvers>`_
        can be used.

        Pypsa also allows using its own solver. Archieved by passing ``pypsa``.

        Note
        ----
        In case the link above is servered, use the pyomo command::

            pyomo help --solvers

    kwargs:
        Keywords parameterizing the solver used as well as the energy system
        transformation process.

        Use one of :meth:`lopf's <pypsa.Network.lopf>`
        parameters for tweaking the solver.

    Return
    ------
    Optimized PyPSA system model
        Energy system carrying the optimization results.
    """
    if solver == "pypsa":
        pyomo = False
    else:
        pyomo = True

    kwargs["solver_name"] = solver

    # 5.) Optimize model:
    # supress solver results getting printed to stdout
    with HideStdoutPrinting():
        system_model.lopf(pyomo=pyomo, **kwargs)

    return system_model
