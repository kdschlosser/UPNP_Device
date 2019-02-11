# -*- coding: utf-8 -*-

import requests
import os
from lxml import etree
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse


try:
    from .xmlns import strip_xmlns
    from .service import Service
    from .embedded_device import EmbeddedDevice
    from .instance_singleton import InstanceSingleton
except ImportError:
    from xmlns import strip_xmlns
    from service import Service
    from embedded_device import EmbeddedDevice
    from instance_singleton import InstanceSingleton


class UPNPObject(object):

    def __init__(self, ip, locations, dump=''):
        self.ip_address = ip
        self._devices = {}
        self._services = {}
        for location in locations:
            parsed = urlparse(location)
            url = '{0}://{1}:{2}/'.format(
                parsed.scheme,
                parsed.hostname,
                parsed.port
            )
            response = requests.get(location)
            content = response.content.decode('utf-8')

            path = parsed.path
            if path.startswith('/'):
                path = path[1:]

            if '/' in path:
                path, file_name = path.rsplit('/', 1)
            else:
                file_name = path
                path = ''

            if not file_name.endswith('.xml'):
                file_name += '.xml'

            if dump:
                if path:
                    output_path = os.path.join(dump, path)

                    if not os.path.exists(output_path):
                        os.makedirs(output_path)
                else:
                    output_path = dump

                temp = ''.join(
                    line.strip() for line in content.split('\n') if
                    line.strip()
                )
                indent = ''
                data = ''
                output = []

                while temp:
                    start = temp.find('<')
                    if start != 0:
                        data = temp[:start]
                        temp = temp[start:]
                    stop = temp.find('>')

                    node = temp[:stop + 1]
                    temp = temp[stop + 1:]

                    if '<?' in node:
                        output += [node]
                    elif '/' in node and data:
                        output[len(output) - 1] += data + node
                        data = ''
                        indent = indent[:-4]
                    elif '/' in node:
                        indent = indent[:-4]
                        output += [indent + node]
                    else:
                        output += [indent + node]
                        indent += '    '

                with open(os.path.join(output_path, file_name), 'w') as f:
                    f.write('\n'.join(output))

            try:
                root = etree.fromstring(content)
            except etree.XMLSyntaxError:
                continue

            root = strip_xmlns(root)
            node = root.find('device')
            if node is None:
                services = []
                devices = []

            else:
                services = node.find('serviceList')

                if services is None:
                    services = []

                devices = node.find('deviceList')
                if devices is None:
                    devices = []

            for service in services:
                scpdurl = service.find('SCPDURL').text.replace(url, '')

                if '/' not in scpdurl and path and path not in scpdurl:
                    scpdurl = path + '/' + scpdurl

                control_url = service.find('controlURL').text
                if control_url is None:
                    if scpdurl.endswith('.xml'):
                        control_url = scpdurl.rsplit('/', 1)[0]
                        if control_url == scpdurl:
                            control_url = ''
                    else:
                        control_url = scpdurl
                else:
                    control_url = control_url.replace(url, '')

                if control_url.startswith('/'):
                    control_url = control_url[1:]

                service_id = service.find('serviceId').text
                service_type = service.find('serviceType').text

                service = Service(
                    self,
                    url,
                    scpdurl,
                    service_type,
                    control_url,
                    node,
                    dump=dump
                )
                name = service_id.split(':')[-1]
                service.__name__ = name
                self._services[name] = service

            for device in devices:
                device = EmbeddedDevice(
                    url,
                    node=device,
                    parent=self,
                    dump=dump
                )
                self._devices[device.__name__] = device

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if item in self._devices:
            return self._devices[item]

        if item in self._services:
            return self._services[item]

        if item in self.__class__.__dict__:
            if hasattr(self.__class__.__dict__[item], 'fget'):
                return self.__class__.__dict__[item].fget(self)

        raise AttributeError(item)

    @property
    def as_dict(self):
        res = dict(
            services=list(service.as_dict for service in self.services),
            devices=list(device.as_dict for device in self.devices)
        )
        return res

    @property
    def access_point(self):
        return self.__class__.__name__

    @property
    def services(self):
        return list(self._services.values())[:]

    @property
    def devices(self):
        return list(self._devices.values())[:]

    def __str__(self):
        output = '\n\n' + str(self.__name__) + '\n'
        output += 'IP Address: ' + self.ip_address + '\n'
        output += '==============================================\n'

        if self.services:
            output += 'Services:\n'
            for cls in self.services:
                output += cls.__str__(indent='    ').rstrip() + '\n'
        else:
            output += 'Services: None\n'

        if self.devices:
            output += 'Devices:\n'
            for cls in self.devices:
                output += cls.__str__(indent='    ').rstrip() + '\n'
        else:
            output += 'Devices: None\n'

        return output
