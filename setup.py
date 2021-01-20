import os

from setuptools import setup, find_packages


def strip_comments(l):
    return l.split('#', 1)[0].strip()


def _pip_requirement(req):
    if req.startswith('-r '):
        _, path = req.split()
        return reqs(*path.split('/'))
    return [req]


def _reqs(*f):
    return [
        _pip_requirement(r) for r in (
            strip_comments(l) for l in open(
            os.path.join(os.getcwd(), 'requirements', *f)).readlines()
        ) if r]


def reqs(*f):
    return [req for subreq in _reqs(*f) for req in subreq]


def get_requirements(*requirements_file):
    """Get the contents of a file listing the requirements"""
    lines = open(os.path.join(os.getcwd(), 'requirements', *requirements_file)).readlines()
    dependencies = []
    for line in lines:
        maybe_dep = line.strip()
        if maybe_dep.startswith('#'):
            # Skip pure comment lines
            continue
        if maybe_dep.startswith('git+'):
            # VCS reference for dev purposes, expect a trailing comment
            # with the normal requirement
            __, __, maybe_dep = maybe_dep.rpartition('#')
        else:
            # Ignore any trailing comment
            maybe_dep, __, __ = maybe_dep.partition('#')
        # Remove any whitespace and assume non-empty results are dependencies
        maybe_dep = maybe_dep.strip()
        if maybe_dep:
            dependencies.append(maybe_dep)
    return dependencies

setup(name='pymongo-ssh',
      version='0.0.3',
      url='https://github.com/pualien/pymongo-ssh',
      license='MIT',
      author='Matteo Senardi',
      author_email='pualien@gmail.com',
      description='Python utilities to simplify connection with MongoDB through SSH tunnel',
      packages=find_packages(exclude=['tests']),
      install_requires=get_requirements('default.txt'),
      long_description=open('README.rst').read(),
      zip_safe=False)
