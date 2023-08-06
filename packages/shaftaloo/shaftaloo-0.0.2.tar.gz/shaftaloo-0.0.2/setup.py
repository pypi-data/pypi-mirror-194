from setuptools import find_packages,setup

setup(
    name = "shaftaloo",
    description= "An open-source python package",
    long_description="asd",
    url= "https://github.com/mohammadamint/shaftaloo/",
    version = "0.0.2",
    packages= find_packages(),
    license="European Union Public License 1.2",
    python_requires = ">=3.6.0",
    package_data={"": ["*.txt", "*.dat", "*.doc", "*.rst","*.xlsx"]},
    install_requires = [
        "pandas >= 1.3.3",
        "numpy >= 1.21.2",
        "xlsxwriter >= 1.3.7",
        "matplotlib >= 3.3.4",
        "openpyxl >= 3.0.6",
        "tqdm",
    ],


)
