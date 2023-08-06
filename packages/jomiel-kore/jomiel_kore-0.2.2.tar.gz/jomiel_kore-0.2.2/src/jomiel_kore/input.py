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
from deprecated import deprecated


@deprecated(reason="use `process_input`, instead")
def read_input(**kwargs):
    """Reads input from, either, the command line (nargs returned by
    configargparse) or directly from stdin. The input is parsed for URIs
    -- and if requested, made sure that they are of proper standard.

    Defaults to stdin (if argv is empty or undefined).

    Ignores the comments, for example:

        # A comment line.
        https://foo     # Also ignored.

    Args:
        **kwargs: arbitrary keyword args

    Supported arbitrary keyword args (kwargs):

        nargs (list): As returned by ConfigArgParse, if none is given,
               the input is read from the stdin, instead

        validate_uri (bool): If True, validates that each item is an URI
            Default is False.

        rebuild_uri (bool): If True (default), each item is rebuilt as an URI.
            Useful if you want to make sure that the URIs look
            representable, fixes various URI string presentation issues
            (e.g. 'HtTpS' -> 'https').

            Ignored, unless used together with validate_uri. Default is
            True.

        components_only (bool): If True, each item is returned as a
            list of broken down URI components.

            Also, when True, forces validate_uri (True) and rebuild_uri
            (False). Default is False.

        unique_items_only (bool): If True (default), returns only the
            unique items. Default is True.

    Raises:
        ValueError if validation is enabled and fails (e.g. the input
        contains entries that do not appear to be HTTP URIs)

    Returns:
        list: Parsed values

    """
    unique_items_only = kwargs.get("unique_items_only", True)
    components_only = kwargs.get("components_only", False)
    validate_uri = kwargs.get("validate_uri", False)
    rebuild_uri = kwargs.get("rebuild_uri", True)
    nargs = kwargs.get("nargs")

    rebuild_uri = False if components_only else rebuild_uri
    validate_uri = True if components_only else validate_uri

    if validate_uri:
        from urllib.parse import urlparse, urlunparse

    def parse():
        """Parse input for URIs."""

        def add(value):
            """Append a new value to the results."""

            if validate_uri:

                uri_components = urlparse(value)
                sch = uri_components.scheme

                if not sch.startswith("http"):
                    raise ValueError("%s: not a valid URI" % value)

                if rebuild_uri:
                    value = urlunparse(uri_components)

                if components_only:
                    value = uri_components

            result.append(value)

        result = []
        if nargs:
            for narg in nargs:
                add(narg)
        else:

            def read_stdin():
                """Read from stdin."""
                from sys import stdin

                while True:
                    line = stdin.readline().strip()
                    if not line:
                        break
                    line = line.split("#", 1)[0].strip()
                    if line:
                        add(line)

            read_stdin()
        return result

    result = parse()
    if unique_items_only:

        def unique_items(seq):  # https://stackoverflow.com/a/480227
            """Return unique items in the results, only."""
            seen = set()
            seen_add = seen.add
            return [s for s in seq if not (s in seen or seen_add(s))]

        return unique_items(result)
    return result


def process_input(**kwargs):
    """Return valid URIs read from either the array of args (nargs) or
    the standard input (stdin). Defaults to reading from the stdin.

    When reading from the stdin, a hash ('#') can be used for comments.
    For example:

        # This is a comment line, and ignored.
        https://foo  # also ignored.
        https://bar
        # https://baz

    Args:
        **kwargs: arbitrary keyword args

    Supported arbitrary keyword args (kwargs):

        nargs (list): the so called "leftover args" typically returned
            by command-line arg parsers after parsing the CLI options.
            If none is given (or the array is empty), then read, process
            and store the input from the stdin, instead.

        http_only (bool): raise an error when True and URI schema is
            anything else but "http/s".

        rebuild_uri (bool): if True, rebuilds each item from the URI
            components. Useful when you want to "cleanup" the URI. e.g.:
            schema "HtTPs" -> "https".

        return_as_objects (bool): if True, the result array will contain
            URI objects (`urllib.parse.ParseResult`) instead of strings.
            Ignores the `rebuild_uri` value.

        unique_items_only (bool): if True, the result list will only
            hold unique values.

    Raises:
        ValueError: if the item was
            - not of supported protocol (HTTP/S), see `http_only`
            - not a valid URI

    Returns:
        list: a list of valid URIs

    """
    from urllib.parse import urlparse, urlunparse
    from validators import url as is_uri

    options = {
        "nargs": None,
        "http_only": True,
        "rebuild_uri": True,
        "return_as_objects": False,
        "return_unique_items": True,
    }
    options.update(kwargs)

    options["rebuild_uri"] = (
        False
        if options["return_as_objects"]
        else options["rebuild_uri"]
    )

    def add_item(value):
        """Store item to the `result` list if it qualifies.

        Args:
            value (str): the URI

        """
        if not value or len(value) == 0:
            return

        if not is_uri(value):
            raise ValueError(f"'{value}' is not a valid URI")

        uri = urlparse(value)

        if options["http_only"] and not uri.scheme.startswith("http"):
            raise ValueError(
                f"{uri.scheme} unsupported protocol ({value})",
            )

        if options["rebuild_uri"]:
            value = urlunparse(uri)

        if options["return_as_objects"]:
            value = uri

        result.append(value)

    nargs = options.get("nargs", None)
    result = []

    if nargs and len(options["nargs"]) > 0:
        for narg in nargs:
            add_item(narg)
    else:

        def from_stdin():
            from sys import stdin

            for ln in stdin:
                ln = ln.split("#", 1)[0].strip()
                add_item(ln)

        from_stdin()

    if options["return_unique_items"]:
        result = list(dict.fromkeys(result))

    return result


if __name__ == "__main__":
    from configargparse import get_parser

    parser = get_parser(add_config_file_help=False)
    parser.add(
        "-t",
        "--http-only",
        help="Expect URIs to be HTTP/S URI strings",
        action="store_true",
        default=True,
    )
    parser.add(
        "-T",
        "--no-http-only",
        dest="http_only",
        action="store_false",
    )
    parser.add(
        "-r",
        "--rebuild-uri",
        help="Rebuild each item from the URI components",
        action="store_true",
        default=True,
    )
    parser.add(
        "-R",
        "--no-rebuild-uri",
        dest="rebuild_uri",
        action="store_false",
    )
    parser.add(
        "-o",
        "--return-as-objects",
        help="Return URIs as objects (urllib.parse.ParseResult)",
        action="store_true",
    )
    parser.add(
        "-O",
        "--no-return-as-objects",
        dest="return_as_objects",
        action="store_false",
    )
    parser.add(
        "-u",
        "--return-unique-items",
        help="Return only unique values",
        action="store_true",
        default=True,
    )
    parser.add(
        "-U",
        "--no-return-unique-items",
        dest="return_unique_items",
        action="store_false",
    )
    parser.add("uri", nargs="*")
    args = parser.parse().__dict__
    try:
        result = process_input(**args, nargs=args["uri"])
        for uri in result:
            print(uri)
    except Exception as error:
        from sys import exit

        print(f"error: {error}")
        exit(1)
    except KeyboardInterrupt:
        pass

# vim: set ts=4 sw=4 tw=72 expandtab:
