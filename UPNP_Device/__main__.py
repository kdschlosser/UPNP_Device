# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import logging
import UPNP_Device


def main():
    parser = argparse.ArgumentParser(prog='UPNP_Deevice')
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        help="increase output verbosity"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=5,
        help="discover timeout in seconds"
    )
    parser.add_argument(
        "ips",
        nargs="*",
        default=[],
        help="optional - ip addresses"
    )

    args = parser.parse_args()

    if not args.verbose:
        log_level = logging.ERROR
    elif args.verbose == 1:
        log_level = logging.INFO
    else:
        log_level = logging.DEBUG

    if not args.ips:
        for device in UPNP_Device.discover(args.timeeout, log_level):
            print(device)
    else:
        for ip in args.ips:
            devices = UPNP_Device.discover(args.timeeout, log_level, ip)

            if devices:
                device = devices[0]
                print(device)
            else:
                logging.error('device at ip %s is not found', ip)


if __name__ == "__main__":
    main()


