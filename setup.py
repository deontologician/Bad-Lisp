from setuptools import setup, find_packages, Command

class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys,subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)

setup(name='badlisp',
      version='0.1a',
      description='An implementation of lisp, given no real experience with '
      'lisp, from a half remembered version of its overall concept',
      author='Josh Kuhn',
      author_email='deontologician@gmail.com',
      url='github.com/habitue01/Bad-Lisp',
      packages=find_packages(),
      cmdclass = {'test' : PyTest}, 
      install_requires = ['pyparsing']
)
