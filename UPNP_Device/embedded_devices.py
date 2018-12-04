

class EmbededDevice(object):
    def __init__(self, node):
        self.services = {}
        self.devices = {}

        services = node.find(device_xmlns('serviceList')) or []
        devices = node.find(device_xmlns('deviceList')) or []
        self._node = node

        for service in services:
            scpdurl = service.find(device_xmlns('SCPDURL')).text
            control_url = service.find(device_xmlns('controlURL')).text
            service_id = service.find(device_xmlns('serviceId')).text
            service_type = service.find(device_xmlns('serviceType')).text

            url = 'http://' + control_url.replace('http://', '').split('/')[0]
            scpdurl = scpdurl.replace(url, '')

            service = Service(url, scpdurl, service_type, control_url)
            name = service_id.split(':')[-1]
            service.__name__ = name
            attr_name = ''
            last_char = ''

            for char in list(name):
                if char.isdigit():
                    continue

                if char.isupper():
                    if attr_name and not last_char.isupper():
                        attr_name += '_'

                if last_char.isupper():
                    last_char = ''
                else:
                    last_char = char
                attr_name += char.lower()

            setattr(self, attr_name, service)
            self.services[name] = service

        for device in devices:
            device = UPNPDevice(device)
            self.devices[device.friendly_name] = device

    def __str__(self, indent=''):
        output = indent + self.friendly_name + '\n'
        output += indent + self.manufacturer + '\n'

        for name, service in self.services.items():
            output += service.__str__(indent=indent + '    ') + '\n'

        output += '\n\n'

        for name, device in self.devices.items():
            output += device.__str__(indent=indent + '    ') + '\n'

        return output

    def __get_tag(self, tag):
        item = self._node.find(device_xmlns(tag))
        if item is None:
            return 'Unknown'
        else:
            return item.text if item.text else 'Unknown'

    @property
    def device_type(self):
        return self.__get_tag('deviceType')

    @property
    def friendly_name(self):
        return self.__get_tag('friendlyName')

    

    @property
    def manufacturer(self):
        return self.__get_tag('manufacturer')

    @property
    def model_name(self):
        return self.__get_tag('modelName')

    @property
    def udn(self):
        return self.__get_tag('UDN')

