"""Wrapping the calliope optimization process."""
import os

from tessif.frused.paths import tessif_dir


def optimize(system_model, solver="cbc", save=False, **kwargs):
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
    system_model.run_config.update({"solver": solver})

    # assuming that the energy system should be run again when the simulate function is called,
    # no matter if it already has been run before or not
    system_model.run(force_rerun=True, **kwargs)

    # cannot overwrite saves. So this only works the first time the model is run.
    if save:
        write_dir = os.path.join(tessif_dir, "tessif-calliope-0-6-6post1")
        system_model.to_csv(
            os.path.join(
                write_dir,
                "Calliope",
                f"{system_model.model_config['name']}_csv",
            ),
        )

    return system_model
