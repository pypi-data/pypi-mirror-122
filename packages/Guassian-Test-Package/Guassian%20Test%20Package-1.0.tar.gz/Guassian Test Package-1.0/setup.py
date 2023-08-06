import setuptools
from pathlib import Path

ROOT_DIR = Path(__file__).parent.resolve()
REQUIREMENTS_DIR = ROOT_DIR / 'requirements'
print(ROOT_DIR)


def read_requirements(fname="requirements.txt"):
    with open(REQUIREMENTS_DIR / fname, 'r') as file:
        return file.read().splitlines()


setuptools.setup(name='Guassian Test Package',
                 version='1.0',
                 description='Nakul Python Gaussian Test Package',
                 author='Nakul Bajaj',
                 author_email='bajaj.nakul@gmail.om',
                 url='https://www.github.com/Nakulbajaj101/gaussian-test-package',
                 packages=['distributions'],
                 package_dir={'distributions': 'distributions'},
                 package_data={'distributions': ['*.txt']},
                 install_requires=read_requirements(),
                 python_requires=">=3.8",
                 license="MIT",
                 classifiers=["License :: OSI Approved :: MIT License",
                              "Programming Language :: Python :: 3",
                              "Programming Language :: Python :: 3.6",
                              "Programming Language :: Python :: 3.7",
                              "Programming Language :: Python :: 3.8",
                              ],
                 )
