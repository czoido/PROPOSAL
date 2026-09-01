import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import rmdir
from conan.tools.microsoft import is_msvc
from conan.tools.scm import Version

required_conan_version = ">=2.0"


class PROPOSALConan(ConanFile):
    name = "proposal"
    homepage = "https://github.com/tudo-astroparticlephysics/PROPOSAL"
    license = "LGPL-3.0"
    package_type = "library"
    description = "Monte Carlo simulation library to propagate leptons and gamma rays"
    topics = ("propagator", "lepton", "photon", "stochastic")

    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_python": [True, False],
        "with_testing": [True, False],
        "with_documentation": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_python": False,
        "with_testing": False,
        "with_documentation": False,
    }

    @property
    def _min_cppstd(self):
        return "14"

    @property
    def _minimum_compilers_version(self):
        return {
            "msvc": "191",
            "gcc": "5",
            "clang": "5",
            "apple-clang": "5",
        }

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)
        self.folders.generators = "build"

    def requirements(self):
        # cubicinterpolation: headers are transitively included, and function calls are made
        # from implementation in headers (templates)
        self.requires("cubicinterpolation/0.1.5", transitive_headers=True, transitive_libs=True)
        # spdlog: requires transitive_libs due to direct calls to functionality from headers
        self.requires("spdlog/1.11.0", transitive_headers=True, transitive_libs=True)
        # nlohmann_json: public headers include json.hpp and json_fwd.hpp
        self.requires("nlohmann_json/3.11.2", transitive_headers=True)
        if self.options.with_python:
            self.requires("pybind11/2.13.6")
        if self.options.with_testing:
            self.requires("boost/1.85.0")
            self.requires("gtest/1.16.0")
        if self.options.with_documentation:
            self.requires("doxygen/1.8.20")

    def validate(self):
        if is_msvc(self) and self.options.shared:
            raise ConanInvalidConfiguration(
                "Can not build shared library on Visual Studio."
            )
        if self.settings.compiler.get_safe("cppstd"):
            check_min_cppstd(self, self._min_cppstd)

        minimum_version = self._minimum_compilers_version.get(
            str(self.settings.compiler), False
        )
        if minimum_version and Version(self.settings.compiler.version) < minimum_version:
            raise ConanInvalidConfiguration(
                f"{self.ref} requires C++{self._min_cppstd}, which your compiler does not support"
            )

    def generate(self):
        tc = CMakeToolchain(self)
        # tc.variables, not tc.cache_variables: cache variables are only written to
        # CMakePresets.json, and cpp.yml configures CMake by hand passing nothing but
        # -DCMAKE_TOOLCHAIN_FILE, so it would never see them.
        tc.variables["BUILD_TESTING"] = bool(self.options.with_testing)
        tc.variables["BUILD_PYTHON"] = bool(self.options.with_python)
        tc.variables["BUILD_DOCUMENTATION"] = bool(self.options.with_documentation)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        if self.options.with_python and not self.options.shared:
            # conan-py-build copies the whole package folder into the wheel, and the
            # wheel only needs the proposal extension module that pyPROPOSAL installs
            # at the root. Drop the C++ SDK artifacts (static library, headers, the
            # exported CMake config) that cmake.install() also stages. Only safe for a
            # static build: shared puts libPROPOSAL in lib/, where the module needs it.
            rmdir(self, os.path.join(self.package_folder, "lib"))
            rmdir(self, os.path.join(self.package_folder, "include"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "PROPOSAL")
        self.cpp_info.set_property("cmake_target_name", "PROPOSAL::PROPOSAL")
        self.cpp_info.libs = ["PROPOSAL"]
