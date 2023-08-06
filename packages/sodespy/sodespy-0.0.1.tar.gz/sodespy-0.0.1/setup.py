import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sodespy",
    version="0.0.1",
    author="mpkuperman",
    author_email="mpkuperman@gmail.com",
    description="SodesPy (Stochastic Ordinary Differential Equations Suite in Python) is a high-performance library for numerically solving stochastic differential equations (SDEs).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mpkuperman/sodespy",
    project_urls={
        "Bug Tracker": "https://github.com/mpkuperman/sodespy/issues",
    },
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)