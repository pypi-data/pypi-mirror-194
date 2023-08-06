from setuptools import setup
setup(name="customized_table",
    version="0.1.7",
    author="Johan Hagelbäck",
    author_email="johan.hagelback@gmail.com",
    description="Creates flexible tables in Jupyter Notebooks with lots of formatting options",
    long_description="Creates flexible tables in Jupyter Notebooks with lots of formatting options such as changing font, font color, cell background, number formatting and much more. Tables can also be saved to csv or Excel files, or generated from csv data files.",
    license="MIT",
    packages=["customized_table"],
    url="https://github.com/jhagelback/customized_table",
    install_requires=["termcolor"]
    )
