#
# jomiel-kore
#
# Copyright
#  2019,2021 Toni Gündoğdu
#
#
# SPDX-License-Identifier: Apache-2.0
#
"""TODO."""
import logging.config
from glob import glob
from logging.config import dictConfig
from os.path import expanduser

from ruamel.yaml import YAML


def log_init(config_paths, **kwargs):
    """Initializes the logger.

    Reads the configuration from a (YAML) file.

    Args:
        config_paths: the list of configuration files (YAML) to read
            Stops at the first existing file.

        **kwargs: arbitrary keyword args

    Supported arbitrary keyword args (kwargs):

        ident_must_exist (str): the name (default: None) of the logger
            ident that is expected to be found among the loaded idents.
            The process will exit unless the ident was found.

    Returns:
        str, dict (tuple): the path to the read config file, the
            dictionary holding the identities parsed from the YAML file

    """

    def load_data():
        """Load the logger config data, if files are not found, use a
        a basic config, instead."""

        # Try to load each of the config files at the given paths.
        for path in map(expanduser, config_paths):
            for found in glob(path):
                with open(found) as handle:
                    yaml = YAML(typ="safe")
                    data = yaml.load(handle)
                    dictConfig(data)
                    return (found, data["loggers"])

        def set_fallback():
            from logging import basicConfig, INFO, info

            basicConfig(
                level=INFO,
                format="[%(levelname)s] %(message)s",
            )

            info(f"unable to find {config_paths}")
            info("using basic logging configuration instead")

            return ("<stdlib:basic>", [])

        # None of the files were found. Use a basic config instead.
        return set_fallback()

    config_file, idents = load_data()
    options = {
        "ident_must_exist": None,
    }
    options.update(kwargs)

    if (
        options["ident_must_exist"]
        and options["ident_must_exist"] not in idents
    ):
        from sys import exit

        logging.error(
            f"invalid logger ident value `{options['ident_must_exist']}`",
        )
        logging.error("see the output of --logger-idents")
        exit(1)

    return config_file, idents


if __name__ == "__main__":
    from configargparse import get_parser

    def parse_opts():
        """Parse options."""
        parser = get_parser(add_config_file_help=False)
        parser.add(
            "-f",
            "--logger-config",
            help="Logger configuration file to read",
            metavar="FILE",
            required=True,
        )
        parser.add(
            "-l",
            "--logger-ident",
            help="Specify the logger identity to use",
            metavar="IDENT",
        )
        parser.add(
            "-L",
            "--logger-idents",
            help="Print the logger idents and exit",
            action="store_true",
        )
        return parser.parse()

    opts = parse_opts()

    log_file, idents = log_init(
        [opts.logger_config],
        ident_must_exist=opts.logger_ident,
    )

    if opts.logger_idents:
        from app import dump_logger_identities

        dump_logger_identities(idents)

    lg = logging.getLogger(opts.logger_ident)
    lg.debug("debug level message")
    lg.info("info level message")

# vim: set ts=4 sw=4 tw=72 expandtab:
