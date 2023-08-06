from setuptools import find_namespace_packages, setup

setup(
    name = "alphausblue",
    author = "Alphaus KK",
    author_email = "dev@alphaus.cloud",
    description = "Alphaus KK's Blue API for Python",
    url = "https://github.com/alphauslabs/blue-sdk-python",
    version = "1.0.1",
    packages = find_namespace_packages(),
    python_requires = ">=3.6",
    options = {
        "bdist_wheel": {
            "universal": True
        }
    }
)