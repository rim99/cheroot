import sys
import re
from distutils.command.install import INSTALL_SCHEMES
from distutils.command.build_py import build_py

import setuptools


needs_pytest = {'pytest', 'test'}.intersection(sys.argv)
pytest_runner = ['pytest_runner'] if needs_pytest else []


class cherrypy_build_py(build_py):
    """Custom version of build_py that excludes Python-specific modules"""

    def build_module(self, module, module_file, package):
        python3 = sys.version_info >= (3,)
        if python3:
            exclude_pattern = re.compile('ssl_pyopenssl|'
                                         '_cpcompat_subprocess')
        else:
            exclude_pattern = re.compile('xxx')
        if exclude_pattern.match(module):
            return  # skip it
        return build_py.build_module(self, module, module_file, package)


###############################################################################
# arguments for the setup command
###############################################################################
name = "CherryPy"
version = "7.1.0"
desc = "Object-Oriented HTTP framework"
long_desc = "CherryPy is a pythonic, object-oriented HTTP framework"
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Web Environment",
    "Intended Audience :: Developers",
    "License :: Freely Distributable",
    "Operating System :: OS Independent",
    "Framework :: CherryPy",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.1",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: Implementation",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: Jython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Internet :: WWW/HTTP",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
    "Topic :: Internet :: WWW/HTTP :: WSGI",
    "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    "Topic :: Internet :: WWW/HTTP :: WSGI :: Server",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
]
author = "CherryPy Team"
author_email = "team@cherrypy.org"
url = "http://www.cherrypy.org"
cp_license = "BSD"
packages = [
    "cherrypy", "cherrypy.lib",
    "cherrypy.tutorial", "cherrypy.test",
    "cherrypy.process",
    "cherrypy.scaffold",
    "cherrypy.wsgiserver",
]
data_files = [
    ('cherrypy', [
        'cherrypy/cherryd',
        'cherrypy/favicon.ico',
        'cherrypy/LICENSE.txt',
    ]),
    ('cherrypy/process', []),
    ('cherrypy/scaffold', [
        'cherrypy/scaffold/example.conf',
        'cherrypy/scaffold/site.conf',
    ]),
    ('cherrypy/scaffold/static', [
        'cherrypy/scaffold/static/made_with_cherrypy_small.png',
    ]),
    ('cherrypy/test', [
        'cherrypy/test/style.css',
        'cherrypy/test/test.pem',
    ]),
    ('cherrypy/test/static', [
        'cherrypy/test/static/index.html',
        'cherrypy/test/static/dirback.jpg',
    ]),
    ('cherrypy/tutorial', [
        'cherrypy/tutorial/tutorial.conf',
        'cherrypy/tutorial/README.txt',
        'cherrypy/tutorial/pdf_file.pdf',
        'cherrypy/tutorial/custom_error.html',
    ]),
]
scripts = ["cherrypy/cherryd"]

install_requires = [
    'six',
]

tests_require = [
    'pytest',
    'routes',
    'nose',
]

cmd_class = {
    'build_py': cherrypy_build_py,
}

if sys.version_info >= (3, 0):
    required_python_version = '3.1'
else:
    required_python_version = '2.6'

###############################################################################
# end arguments for setup
###############################################################################

# wininst may install data_files in Python/x.y instead of the cherrypy package.
# Django's solution is at http://code.djangoproject.com/changeset/8313
# See also
# http://mail.python.org/pipermail/distutils-sig/2004-August/004134.html
if 'bdist_wininst' in sys.argv or '--format=wininst' in sys.argv:
    data_files = [(r'\PURELIB\%s' % path, files) for path, files in data_files]

setup_params = dict(
    name=name,
    version=version,
    description=desc,
    long_description=long_desc,
    classifiers=classifiers,
    author=author,
    author_email=author_email,
    url=url,
    license=cp_license,
    packages=packages,
    data_files=data_files,
    scripts=scripts,
    cmdclass=cmd_class,
    install_requires=install_requires,
    # Enables `python setup.py test` invocation install test dependencies first
    tests_require=tests_require,
    setup_requires=[
    ] + pytest_runner,
)


def main():
    if sys.version < required_python_version:
        s = "I'm sorry, but %s %s requires Python %s or later."
        print(s % (name, version, required_python_version))
        sys.exit(1)
    # set default location for "data_files" to
    # platform specific "site-packages" location
    for scheme in list(INSTALL_SCHEMES.values()):
        scheme['data'] = scheme['purelib']

    setuptools.setup(**setup_params)


if __name__ == "__main__":
    main()
