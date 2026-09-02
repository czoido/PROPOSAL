"""Smoke checks for the packaged extension module.

The wheel is a single compiled module, so the failure that matters here is the
quiet one: a binding source that never made it into the build, leaving a whole
submodule missing. src/pyPROPOSAL/CMakeLists.txt collects its sources with
file(GLOB_RECURSE), which CMake evaluates at configure time, so a source that
goes missing does not announce itself.
"""
import proposal as pp
import pytest

# Every submodule the bindings register, nested ones included. Keep in sync with
# the def_submodule calls under src/pyPROPOSAL/detail/.
SUBMODULES = [
    "component",
    "crosssection",
    "decay",
    "density_distribution",
    "geometry",
    "logging",
    "math",
    "medium",
    "medium.PDG2001",
    "medium.PDG2020",
    "parametrization",
    "parametrization.annihilation",
    "parametrization.bremsstrahlung",
    "parametrization.compton",
    "parametrization.ionization",
    "parametrization.mupairproduction",
    "parametrization.pairproduction",
    "parametrization.photoeffect",
    "parametrization.photomupair",
    "parametrization.photonuclear",
    "parametrization.photopair",
    "parametrization.photoproduction",
    "parametrization.weakinteraction",
    "particle",
    "scattering",
    "secondaries",
]


@pytest.mark.parametrize("path", SUBMODULES)
def test_submodule_is_reachable_and_populated(path):
    obj = pp
    for part in path.split("."):
        assert hasattr(obj, part), f"proposal.{path} is missing"
        obj = getattr(obj, part)
    assert [n for n in dir(obj) if not n.startswith("_")], \
        f"proposal.{path} registered nothing"


def test_objects_from_several_binding_modules_can_be_built():
    # One construction per binding source, so a submodule that is present but
    # unusable does not pass as working.
    assert pp.particle.MuMinusDef().name == "MuMinus"
    assert pp.medium.Ice().mass_density > 0
    assert pp.EnergyCutSettings(500, 0.05).ecut == 500
    assert pp.geometry.Sphere(pp.Cartesian3D(0, 0, 0), 1e20) is not None
    assert pp.PropagationUtilityCollection() is not None
