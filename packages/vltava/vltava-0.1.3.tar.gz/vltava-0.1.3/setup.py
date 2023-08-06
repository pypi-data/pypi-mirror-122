import setuptools
import pathlib

VERSION = "0.1.3"

INSTALL_REQUIRES = [
    "majka>=0.8",
    "ufal.morphodita>=1.10.1.1",
    "gensim>4",
]

EXTRAS_REQUIRE = {"tests": ["pytest"]}


def run_setup():
    """
    Runs the package setup.
    """
    
    this_directory = pathlib.Path(__file__).parent

    setup_params = {
        "name": "vltava",
        "version": VERSION,
        "description": "Opinionated Czech Language Processing",
        "author": "Jan Cervenka",
        "author_email": "jan.cervenka@yahoo.com",
        "long_description": (this_directory / "README.md").read_text(),
        "long_description_content_type": "text/markdown",
        "package_dir": {"": "src"},
        "packages": setuptools.find_packages(where="src"),
        "include_package_data": True,
        "package_data": {"": ["*.stopwords", "*.w-lt", "*.dict"]},
        "python_requires": ">=3.7",
        "install_requires": INSTALL_REQUIRES,
        "extras_require": EXTRAS_REQUIRE,
    }
    setuptools.setup(**setup_params)


if __name__ == "__main__":
    run_setup()
