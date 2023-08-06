import os
import sys

import argparse

from evidence.Controller import Controller
from evidence.phase.PrepareEvidence import PrepareEvidence
from evidence.phase.MergeEvidence import MergeEvidence
from evidence.phase.CharacterizeEvidence import CharacterizeEvidence

def main(args_=None):
    """The main routine."""
    if args_ is None:
        args_ = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument("--path", "-p", type=str, required=True, help="Path to idifference output dir")
    parser.add_argument("--output", "-o", type=str, default="output", help="Path to result dir")
    args = parser.parse_args()

    ctrl = Controller(output = args.output)
    ctrl.scaffold()

    # Prepare Evidence Phase

    pe = PrepareEvidence()

    for path, dirs, files in os.walk(args.path):
        for file in files:
            pe.process(path, file, ctrl.pathPE)

    # Merge Evidence Phase

    me = MergeEvidence()

    # Characterize Evidence Phase

    ce = CharacterizeEvidence()


if __name__ == "__main__":
    sys.exit(main())
