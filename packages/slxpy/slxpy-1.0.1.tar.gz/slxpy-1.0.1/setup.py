import setuptools
from pathlib import Path

cwd = Path(__file__).parent
package_dir = cwd / "slxpy"
package_data = [
    str(f.relative_to(package_dir)) for f in (package_dir / "include").glob("**/*") if f.is_file()
] + [
    str(f.relative_to(package_dir)) for f in (package_dir / "templates").glob("**/*") if f.is_file()
]
long_description = (cwd / "README.md").read_text()

setuptools.setup(
    name='slxpy',
    version='1.0.1',
    description = "Simulink Python binding generator.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    license = "MIT",
    keywords = ["simulink", "c++", "gym"],
    author="Jiang Yuxuan",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Programming Language :: Python"
    ],

    packages=[
        "slxpy",
        "slxpy.common",
        "slxpy.frontend",
        "slxpy.backend",
    ],
    package_data={"slxpy": package_data},

    install_requires=[
        "pybind11",
        "jinja2",
        "rtoml",
        "importlib_resources",
        "Click>=8.0",
    ],
    entry_points={
        'console_scripts': [
            'slxpy = slxpy.cli:entry_point',
        ],
    },
)
