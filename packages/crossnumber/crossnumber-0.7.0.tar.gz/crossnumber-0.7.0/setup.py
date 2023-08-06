from distutils.core import setup
setup(
  name = 'crossnumber',
  packages = ['crossnumber'], # this must be the same as the name above
  install_requires=['numpy', 'termcolor','sympy'],
  version = '0.7.0',
  description = 'A collection of Python functions which may be of use when solving crossnumber puzzles.',
  long_description='A collection of Python functions which may be of use when solving crossnumber puzzles.',
  author = 'Adam Vellender',
  author_email = 'dev@vellender.com',
  url = 'https://github.com/vellender/crossnumber',
  keywords = ['crossnumber','solver','solve','tools','tool','puzzle','listener','magpie','numerical','numericals','crossword','mathematical','mathematicals'], 
  classifiers = [],
)
