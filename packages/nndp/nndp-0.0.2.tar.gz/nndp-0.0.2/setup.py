from setuptools import setup


with open("README.md","r") as fh:
    long_description = fh.read()

setup(
    name = 'nndp',
    version = '0.0.2',
    description = 'Dynamic Programming with Neural Networks',
    long_description = long_description,
    long_description_content_type='text/markdown',
    py_modules = ["nndp.policy_function", "nndp.utils"],
    package_dir={'':'src'},
    author='Marc de la Barrera i Bardalet',
    url = 'https://github.com/marcdelabarrera/nndp',
    author_email='mbarrera@mit.edu',
    install_requires = ["numpy >=1.20.0","jax >= 0.4.0"],
    extras_require={"dev":["pytest>=7.1.2",],},
    classifiers =[
        "Programming Language :: Python :: 3.10"
    ]
)