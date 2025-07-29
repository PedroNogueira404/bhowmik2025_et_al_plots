# setup.py
from setuptools import setup, find_packages

setup(
    name="bhowmik2025_et_al_plots",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        # your dependencies
    ],
    entry_points={
        "console_scripts": ["bhowmik-plotter = bhowmik2025_et_al_plots.plotter:main"]
    },
)
