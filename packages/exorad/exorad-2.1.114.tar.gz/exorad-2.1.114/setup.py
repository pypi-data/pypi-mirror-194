import codecs
import os

from setuptools import setup, find_packages

packages = find_packages(exclude=('tests', 'docs'))

provides = ['exorad', ]
console_scripts = [
    'exorad=exorad.exorad:main',
    'exorad-plot=exorad.utils.plotter:main [Plot]']

with open('/home/lorenzo/git/ExoRad2-public/requirements.txt') as f:
    required = f.read().splitlines()
install_requires = required

entry_points = {'console_scripts': console_scripts, }

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: BSD License',
    'Operating System :: POSIX',
    'Operating System :: POSIX :: Linux',
    'Operating System :: Unix',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Topic :: Scientific/Engineering',
    'Topic :: Software Development :: Libraries',
]


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_info(rel_path, info):
    for line in read(rel_path).splitlines():
        if line.startswith('__%s__' % info):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find %s string." % info)


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='exorad',
      provides=provides,
      version=get_info("exorad/__version__.py", 'version'),
      description=get_info("exorad/__init__.py", 'summary'),
      url=get_info("exorad/__init__.py", 'url'),
      author=get_info("exorad/__init__.py", 'author'),
      author_email=get_info("exorad/__init__.py", 'email'),
      license=get_info("exorad/__init__.py", 'license'),
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=packages,
      classifiers=classifiers,
      install_requires=install_requires,
      include_package_data=True,
      package_data={"exorad/data": ["data/*"]},
      entry_points=entry_points,
      python_requires='>=3.8',
      zip_safe=False)
