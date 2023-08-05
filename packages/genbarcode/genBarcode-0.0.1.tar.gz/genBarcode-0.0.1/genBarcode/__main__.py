#pylint: disable=missing-module-docstring
#from __future__ import (print_function, unicode_literals, division, absolute_import)
__metaclass__ = type
__package_name__ = 'genBarcode'

## Standard Libraries
import os
import sys
import argparse
import logging
from io import BytesIO
from pprint import pprint#, pformat

## Third Party libraries
import pkg_resources
import barcode
from barcode.writer import ImageWriter
from PIL import Image, ImageShow

## Modules
try:
    from .classes import ReturnCodes
    from .classes import CustomExceptions
except ImportError:
    # If we can't import modules, probably running from VSCODE
    # attempt to hack in modules
    import importlib
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(SCRIPT_DIR))
    ReturnCodes = importlib.import_module(__package_name__+'.classes.ReturnCodes')
    CustomExceptions = importlib.import_module(__package_name__+'.classes.CustomExceptions')

## Load up some metadata
try:
    __code_name__  = __package_name__
    # spacing is deliberate
    __code_desc__ = """ program description to be displayed by argparse \n    ex: python {name}
        """.format(name=str(__package_name__)+'.py')
    _distro = pkg_resources.get_distribution(__package_name__)
    __code_version__ = _distro.version
    __code_meta__ = vars(_distro)
    __code_debug__ = False
except pkg_resources.DistributionNotFound:
    # when debugging with vscode
    __code_debug__ = True
    stubs = [ '__code_version__', '__code_meta__']
    for s in stubs:
        globals()[s] = 'Not Available'

def __print_dunders__():
    blacklist = ['__builtins__', '__print_dunders__']
    for k, v in list(globals().items()):
        if k.startswith('__'):
            if k in blacklist:
                pass
            else:
                pprint("%s => %s" % (k, v))

def begin_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            style="{",
            fmt="[{name}:{filename}] {levelname} - {message}"
        )
    )
    log = logging.getLogger(__package_name__)
    log.setLevel(logging.INFO)
    log.addHandler(handler)

def collect_args():
    parser = argparse.ArgumentParser(description=__code_desc__,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-V', '--version', action='version', version=__code_version__)
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-l', '--list-methods', action='store_true',
        help="Enumerate available generators and exit")
    parser.add_argument('-m', '--method', default='code128',
        help="set the barcode generated type (default: %(default)s)")
    parser.add_argument('-d', '--data', help="Provide data to be used to generate the barcode")
    parser.add_argument('-t', '--tracking',
        help="Provide tracking number to be used to generate the barcode, stub for --data")
    args = parser.parse_args()
    return parser, args

def handle_args():
    parser, args = collect_args()
    methods = barcode.PROVIDED_BARCODES

    if args.list_methods:
        pprint(methods)
        sys.exit(0)

    if args.method:
        if args.method not in methods:
            raise AssertionError("%s not in acceptable methods (%s)" % (args.method, methods))

    if args.data is None and args.tracking is None:
        parser.print_help()
        sys.exit(ReturnCodes.EXIT_USAGE)
    else:
        args.data = args.data or args.tracking
    return args

def demo():
    __print_dunders__()
    sys.exit(ReturnCodes.EXIT_DEMO)

def main():
    begin_logging()
    args = handle_args()

    rv = BytesIO()
    klass = barcode.get_barcode_class(args.method)
    klass(str(args.data), writer=ImageWriter()).write(rv)
    with Image.open(rv) as im:
        try:
            rcode = ImageShow.show(im)
            if rcode:
                return ReturnCodes.EXIT_SUCCESS
            else:
                raise CustomExceptions.NoImageViewerAvailable
        except CustomExceptions.NoImageViewerAvailable:
            # will revisit
            raise NotImplementedError from CustomExceptions.NoImageViewerAvailable

if __name__=="__main__":
    main()
