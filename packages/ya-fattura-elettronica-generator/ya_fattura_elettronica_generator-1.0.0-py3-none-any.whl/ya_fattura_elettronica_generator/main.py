import argparse
import logging
import sys
from typing import List

from ya_fattura_elettronica_generator import version, models
from ya_fattura_elettronica_generator.IFatturaElettronicaValidator import ValidationOutcome
from ya_fattura_elettronica_generator.models import FatturaElettronicaType
from ya_fattura_elettronica_generator.validations import RegimeForfettarioMonthlyInvoiceValidator



def validate_forfettario(args):
    validator = RegimeForfettarioMonthlyInvoiceValidator()
    fattura_elettronica = models.parse(args.file, silence=True, print_warnings=True)
    checks = validator.validate(fattura_elettronica, dict())
    validator.print_validation_summary(checks)

def parse_options(args):

    parser = argparse.ArgumentParser(prog="FatturaElettronicaGenerator", description="""
    Allows you to generate and validate fatture elettroniche
    """, epilog=f"Copyright Massimo Bono 2021, version={version.VERSION}")
    subparsers = parser.add_subparsers(help="choose a subparser to use")

    validate_subparser = subparsers.add_parser("validate", help="Use this if you want to validate a preexisting fattura elettronica XML file")
    validate_subparser.add_argument("-f", "--file", required=True, type=str, help="The fattura elettronica XML you want to validate")
    # validate_subparser.set_defaults(func=validate)

    validate_subparser_subparsers = validate_subparser.add_subparsers(help="Choose a regime you use")

    validate_forfettario_subparser = validate_subparser_subparsers.add_parser("forfettario", help="Your regime is a forfettario one")
    validate_forfettario_subparser.add_argument("-m", "--monthly", action="store_true", help="Use this flag if you send the invoice every month since you offer a monthly service")
    validate_forfettario_subparser.set_defaults(func=validate_forfettario)

    result = parser.parse_args(args)
    return parser, result


def main(args):
    parser, options = parse_options(args)

    logging.basicConfig(level="INFO")

    if not hasattr(options, "func"):
        parser.print_help()
    else:
        options.func(options)


def _main():
    main(sys.argv[1:])


if __name__ == "__main__":
    _main()
