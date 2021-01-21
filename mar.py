import argparse
from version import __version__

parser = argparse.ArgumentParser()

parser.add_argument('--version', action='version', version='%(prog)s {version}'.format(version=__version__))
parser.parse_args()

