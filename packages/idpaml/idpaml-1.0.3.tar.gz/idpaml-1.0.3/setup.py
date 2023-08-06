from setuptools import setup
setup(
    name='idpaml',
    version='1.0.3',
    author='cpaulis2',
    description='AzureML wrapper for disease modeling.',
    long_description='This is a longer description for the project',
    url='https://github.com/uhg-internal/idp-aml',
    keywords='azureml, idp, aml',
    python_requires='>=3.6, <4',
    install_requires=[
        "azure-ai-ml",
        "azure-identity",
        "azure-storage-blob<=12.13.0",
        "hydra-core",
        "opencensus-ext-azure",
        "PyYAML",
        "pyfiglet",
        "pandas",
        "pickle5",  # imported as pickle
        "pyyaml",   # imported as yaml
        ]
)