from setuptools import setup,find_packages
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


project_urls = {
  'Homepage': 'https://pyams.org',
  'Documentation': 'https://pyams.org',
  'Download': 'https://pyams.org/download',
  'Source': "https://github.com/d-fathi/PyAMS"
}


setup(
    name='pyams-lib',
    version='0.0.2',
    description='PyAMS: Python for Analog and Mixed Signals',
    author= 'd.fathi',
    project_urls = project_urls,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['src','library','library.Basic','library.Source','cad','demo','demo_cad','out','out.temp'],
    keywords=['Analog', 'CAD System', 'Simulation circuit','PyAMS'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering"
    ],
    python_requires='>=3.0',
    py_modules=['PyAMS','simu'],
    package_dir={'':'pack','library':'pack/library','library.Basic':'pack/library/Basic','library.Source':'pack/library/Source','cad':'pack/cad','demo':'pack/demo','src':'pack/src','demo_cad':'pack/demo_cad','out':'pack/out','out.temp':'pack/out/temp'},
    install_requires = [
        'matplotlib'
    ],
    package_data={'pack':['*'],'library': ['*'],'library.Basic':['*'],'library.Source': ['*'],'cad': ['*'],'src': ['*'],'cad': ['*'],'demo': ['*'],'demo_cad': ['*'],'out': ['*'],'out.temp': ['*']},
    include_package_data=True
)

