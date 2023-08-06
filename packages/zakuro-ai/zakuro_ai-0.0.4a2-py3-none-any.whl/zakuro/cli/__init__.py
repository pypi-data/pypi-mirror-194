import os
import sys
def main(argv=sys.argv):
    if len(argv)>1:   
        argv = argv[1:]
        os.system(f"python -m zakuro.cli.{argv[0]} {' '.join(argv[1:])}")