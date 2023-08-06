import pathlib
from setuptools import setup,find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="alphavantage-api-cesar",
    version="1.0.5",
    description="Projeto desenvolvido para primeira semana do cesar inova afro bootcamp",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ekdespe/",
    author="Erik Ferreira",
    author_email="ekdespe@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["settings","core","stock_time_series"],
    include_package_data=True,
    install_requires=["requests", "python-decouple"],
    entry_points={
        "console_scripts": [
            "alphavantage=stock_time_series.__main__:main",
        ]
    },
)
