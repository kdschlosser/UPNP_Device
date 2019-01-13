# -*- coding: utf-8 -*-

from __future__ import print_function
import argparse
import logging
import UPNP_Device
import threading
import sys


def main():
    parser = argparse.ArgumentParser(prog='UPNP_Device')
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

    found_devices = []
    event = threading.Event()

    def do():
        if log_level != logging.DEBUG:
            sys.stdout.write('Finding UPNP Devices please wait..')
        else:
            print('Finding UPNP Devices please wait..')

        event.set()

        for device in UPNP_Device.discover(args.timeout, log_level, args.ips):
            found_devices.append(device)
        event.set()

    t = threading.Thread(target=do)
    t.daemon = True
    t.start()

    event.wait()
    event.clear()
    while not event.isSet():
        if log_level != logging.DEBUG:
            sys.stdout.write('.')
        event.wait(1)
    print()

    for dvc in found_devices:
        print(dvc)

    for ip in args.ips:
        for device in found_devices:
            if device.ip_address == ip:
                break
        else:
            logging.error('Unable to locate a device at IP ' + ip)


if __name__ == "__main__":
    main()


