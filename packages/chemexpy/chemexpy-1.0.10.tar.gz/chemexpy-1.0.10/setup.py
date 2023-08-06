import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(name='chemexpy',
      version='1.0.10',
      description='Cheminformatics package for compound feature evaluation',
      author='Auste Kanapeckaite',
      author_email='auste.kan@algorithm379.com',
      url='https://github.com/AusteKan/Chemexpy',
      packages=['chemexpy'],
      license="GNU General Public License version 3",
       include_package_data=True,
       install_requires=["seaborn", "matplotlib","scipy","numpy","pandas"],
        classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent", ],
        python_requires=">=3.6"
        )

