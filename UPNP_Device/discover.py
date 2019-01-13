# -*- coding: utf-8 -*-

from __future__ import print_function
import socket
import threading
import ifaddr
import ipaddress
import sys

import logging


logger = logging.getLogger('UPNP_Devices')

if sys.platform.startswith('win'):
    IPPROTO_IPV6 = 41
else:
    IPPROTO_IPV6 = getattr(socket, 'IPPROTO_IPV6')

IPV4_MCAST_GRP = "239.255.255.250"
IPV6_MCAST_GRP = "[ff02::c]"

IPV4_SSDP = '''M-SEARCH * HTTP/1.1\r
ST: upnp:rootdevice\r
MAN: "ssdp:discover"\r
HOST: 239.255.255.250:1900\r
MX: 1\r
Content-Length: 0\r
\r
'''

IPV6_SSDP = '''M-SEARCH * HTTP/1.1\r
ST: upnp:rootdevice\r
MAN: "ssdp:discover"\r
HOST: [ff02::c]:1900\r
MX: 1\r
Content-Length: 0\r
\r
'''

'''NOTIFY * HTTP/1.1
HOST: 239.255.255.250:1900
CACHE-CONTROL: max-age=1800
LOCATION: http://192.168.1.1:49152/gatedesc_224.xml
OPT: "http://schemas.upnp.org/upnp/1/0/"; ns=01
01-NLS: a578cd9c-440d-11e8-973b-e4f6d5f2e149
NT: urn:schemas-upnp-org:service:WANIPConnection:1
NTS: ssdp:alive
SERVER: Linux/2.6.16.26-Cavium-Octeon, UPnP/1.0, Portable SDK for UPnP devices/1.6.19
X-User-Agent: redsonic
USN: uuid:75802409-bccb-40e7-8e6c-fa095ecce13e::urn:schemas-upnp-org:service:WANIPConnection:1

'''


def discover(timeout=5, log_level=None, search_ips=[]):
    if log_level is not None:
        logging.basicConfig(format="%(message)s", level=log_level)
        if log_level is not None:
            logger.setLevel(log_level)

    # Received 6/11/2018 at 9:38:51 AM (828)
    #
    # HTTP/1.1 200 OK
    # CACHE-CONTROL: max-age = 1800
    # EXT:
    # LOCATION: http://192.168.1.63:52235/rcr/RemoteControlReceiver.xml
    # SERVER: Linux/9.0 UPnP/1.0 PROTOTYPE/1.0
    # ST: urn:samsung.com:device:RemoteControlReceiver:1
    # USN: uuid:2007e9e6-2ec1-f097-f2df-944770ea00a3::urn:samsung.com:device:
    #           RemoteControlReceiver:1
    # CONTENT-LENGTH: 0

    found = {}
    found_event = threading.Event()
    threads = []
    adapter_ips = []

    for adapter in ifaddr.get_adapters():
        for adapter_ip in adapter.ips:
            if isinstance(adapter_ip.ip, tuple):
                # adapter_ips += [adapter_ip.ip[0]]
                continue
            else:
                adapter_ips += [adapter_ip.ip]

    def convert_ssdp_response(packet, addr):
        packet = packet.decode('utf-8').split('\n', 1)[1]

        packet = dict(
            (
                line.split(':', 1)[0].strip().upper(),
                line.split(':', 1)[1].strip()
            ) for line in packet.split('\n') if line.strip()
        )

        if 'LOCATION' in packet:
            logger.debug(
                'SSDP: %s found LOCATION: %s',
                addr,
                packet['LOCATION']
            )

            if 'NT' in packet:
                logger.debug(
                    'SSDP: %s found NT: %s',
                    addr,
                    packet['NT']
                )
            if 'ST' in packet:
                logger.debug(
                    'SSDP: %s found ST: %s',
                    addr,
                    packet['ST']
                )

        return packet

    def send_to(destination, t_out=5):
        try:
            network = ipaddress.ip_network(destination.decode('utf-8'))
        except:
            network = ipaddress.ip_network(destination)

        if isinstance(network, ipaddress.IPv6Network):
            mcast = IPV6_MCAST_GRP
            ssdp_packet = IPV6_SSDP
            sock = socket.socket(
                family=socket.AF_INET6,
                type=socket.SOCK_DGRAM,
                proto=socket.IPPROTO_IP
            )
            sock.setsockopt(IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, 1)

        else:
            mcast = IPV4_MCAST_GRP
            ssdp_packet = IPV4_SSDP
            sock = socket.socket(
                family=socket.AF_INET,
                type=socket.SOCK_DGRAM,
                proto=socket.IPPROTO_UDP
            )
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if destination in adapter_ips:
            sock.bind((destination, 0))
            destination = mcast

        sock.settimeout(t_out)

        logger.debug('SSDP: %s\n%s', destination, ssdp_packet)
        for _ in range(5):
            sock.sendto(ssdp_packet.encode('utf-8'), (destination, 1900))
        return sock

    def do(local_address, target_ips):
        sock = send_to(local_address)

        for target_ip in target_ips:
            found[target_ip] = set()
            t = threading.Thread(target=found_thread, args=(target_ip,))
            t.daemon = True
            threads.append(t)
            t.start()

        while True:
            try:
                data, addr = sock.recvfrom(1024)
            except socket.timeout:
                break

            if target_ips and addr[0] not in target_ips:
                continue

            packet = convert_ssdp_response(data, addr[0])

            if 'LOCATION' not in packet:
                continue

            if addr[0] not in found:
                found[addr[0]] = set()
                t = threading.Thread(target=found_thread, args=(addr[0],))
                t.daemon = True
                threads.append(t)
                t.start()

            found[addr[0]].add(packet['LOCATION'])
        try:
            sock.close()
        except socket.error:
            pass

        threads.remove(threading.current_thread())

        if not threads:
            found_event.set()

    def found_thread(ip):
        sock = send_to(ip, timeout)

        try:
            while True:
                data, addr = sock.recvfrom(1024)

                packet = convert_ssdp_response(data, addr[0])

                if 'LOCATION' not in packet:
                    continue

                logger.debug('SSDP: %s - > %s', addr[0], data)

                found[addr[0]].add(packet['LOCATION'])

        except socket.error:
            pass

        threads.remove(threading.current_thread())

        if not threads:
            found_event.set()

    for adapter_ip in adapter_ips:
        t = threading.Thread(
            target=do,
            args=(adapter_ip, search_ips)
        )
        t.daemon = True
        threads += [t]
        t.start()

    found_event.wait()

    for ip, locations in found.items():
        locations = list(loc for loc in locations)
        if not locations:
            continue

        yield ip, locations


if __name__ == '__main__':
    from upnp_class import UPNPObject

    from logging import NullHandler

    logger.addHandler(NullHandler())

    for device_ip, locs in discover(5, logging.DEBUG):
        print(UPNPObject(device_ip, locs))
