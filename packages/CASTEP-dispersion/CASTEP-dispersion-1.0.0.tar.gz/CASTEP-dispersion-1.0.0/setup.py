from setuptools import find_packages
from setuptools import setup,Extension

setup(name="CASTEP-dispersion",
      version="1.0.0",
      packages=find_packages(),
      description="CASTEP utility for plotting band structures and phonon dispersions.",
      url="https://github.com/zachary-hawk/dispersion.py.git",
      author="Zachary Hawkhead",
      author_email="zachary.hawkhead@durham.ac.uk",
      license="MIT",
      install_requires=["numpy",
                        "matplotlib",
                        "fractions",
                        "ase>=3.18.1",
                        "itertools",
                        "argparse"],

      entry_points={"console_scripts":["dispersion.py=main:main",]
                    }

      )



