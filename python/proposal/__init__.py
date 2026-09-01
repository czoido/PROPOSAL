"""Monte Carlo simulation library to propagate leptons and gamma rays.

The whole API lives in the compiled extension module ``proposal._proposal`` and is
re-exported here, so ``import proposal`` keeps working as before.
"""

import sys as _sys
from types import ModuleType as _ModuleType

from . import _proposal as _ext
from ._proposal import *  # noqa: F401,F403

# Keep in sync with PROPOSAL_VERSION_* in CMakeLists.txt.
__version__ = "7.6.2"


def _alias_submodules(module, public_prefix):
    """Alias the pybind11 submodules of ``module`` under ``public_prefix``.

    pybind11 registers them in ``sys.modules`` as ``proposal._proposal.<name>``.
    Aliasing them to ``proposal.<name>`` keeps ``import proposal.particle`` working,
    as it did when the extension itself was the top-level ``proposal`` module.
    """
    for name, value in vars(module).items():
        if isinstance(value, _ModuleType) and value.__name__ == f"{module.__name__}.{name}":
            public_name = f"{public_prefix}.{name}"
            _sys.modules[public_name] = value
            _alias_submodules(value, public_name)


_alias_submodules(_ext, __name__)
