from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        "_ckmeans_1d_dp",
        [
            "python/_ckmeans_1d_dp.cpp",
            "src/Ckmeans.1d.dp.cpp",
            "src/dynamic_prog.cpp",
            "src/EWL2_dynamic_prog.cpp",
            "src/EWL2_fill_log_linear.cpp",
            "src/EWL2_fill_quadratic.cpp",
            "src/EWL2_fill_SMAWK.cpp",
            "src/fill_log_linear.cpp",
            "src/fill_quadratic.cpp",
            "src/fill_SMAWK.cpp",
            "src/select_levels.cpp",
            "src/weighted_select_levels.cpp",
        ],
    ),
]

setup(
    package_dir = {"ckmeans_1d_dp" : "python"},
    cmdclass = {"build_ext": build_ext},
    ext_modules = ext_modules,
)
