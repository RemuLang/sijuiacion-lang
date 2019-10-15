import sys
from importlib import import_module
from wisepy2 import wise



@wise
def cli(*, file=''):
    if file:
        import_module("test." + file)

if __name__ == '__main__':
    cli(sys.argv[1:])