from setuptools import setup, find_namespace_packages


APP_NAME = "mlflow_cortex"
VERSION = "1.10.0"
AUTHOR = "Matthew Grohotolski"
DESCRIPTION = "MLflow model flavor for mlflow_cortex with keras custom object integration"

setup(
    name=APP_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESCRIPTION,
    install_requires=[
        "mlflow>=1.11.0",
    ],
    extras_require={},
    packages=find_namespace_packages("src"),
    package_dir={"": "src"},
    entry_points="""
    [console_scripts]
    """,
    python_requires=">=3.8.13",
)
