import setuptools

exec(open("tc_grain/_version.py").read())

setuptools.setup(
    name="tc-grain",
    version=__version__,
    packages=setuptools.find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "chemcloud",
        "tcpb-trio",
        "trio",
    ],
    extras_require={
        "dev": [
            "black",
            "pre-commit",
        ],
    },
    tests_require=[],
    entry_points={
        "console_scripts": ["tcpb_grain_spawn=tc_grain.util:tcpb_spawn"],
    },
)
