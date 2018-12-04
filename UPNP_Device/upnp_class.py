import sys
import six
import requests
from xml.etree import cElementTree as ElementTree
from . import xmlns
from .service import Service
from .icon import Icon


PY3 = sys.version_info[0] >= 3


class UPNPSingleton(type):
    _objects = {}

    def __call__(
        cls,
        ip,
        classes
    ):

        if ip not in UPNPSingleton._objects:
            UPNPSingleton._objects[ip] = (
                super(UPNPSingleton, cls).__call__(ip, classes)
            )

        return UPNPSingleton._objects[ip]


@six.add_metaclass(UPNPSingleton)
class UPNPObject(object):

    def __init__(self, ip, classes):

        self.ip_address = ip
        url_template = b'http://'
        cls_name = None
        self.__devices = {}
        self.__services = {}

        for cls, location in classes.items():
            url = url_template + (
                location.replace(b'http://', b'').split(b'/')[0]
            )
            location = location.replace(url, b'')

            response = requests.get(url + location)
            root = ElementTree.fromstring(response.content)
            node = root.find(xmlns.device_xmlns('device'))

            services = node.find(xmlns.device_xmlns('serviceList')) or []
            devices = node.find(xmlns.device_xmlns('deviceList')) or []

            for service in services:
                scpdurl = service.find(
                    xmlns.device_xmlns('SCPDURL')
                ).text
                control_url = service.find(
                    xmlns.device_xmlns('controlURL')
                ).text
                service_id = service.find(
                    xmlns.device_xmlns('serviceId')
                ).text
                service_type = service.find(
                    xmlns.device_xmlns('serviceType')
                ).text
                if location is None:
                    scpdurl = scpdurl.encode('utf-8')
                else:
                    scpdurl = (
                        b'/' +
                        location[1:].split(b'/')[0] +
                        b'/' +
                        scpdurl.encode('utf-8')
                    )

                service = Service(
                    self,
                    url,
                    scpdurl,
                    service_type,
                    control_url,
                    node
                )
                name = service_id.split(':')[-1]
                service.__name__ = name
                self.__services[name] = service

            for device in devices:
                device = UPNPDevice(url, node=device, parent=self)
                self.__devices[device.__name__] = device

            if cls_name is None:
                cls_name = node.find(xmlns.device_xmlns('modelName'))
                if cls_name is not None and cls_name.text:
                    cls_name = cls_name.text.replace(' ', '_').replace('-', '')

        self.__name__ = cls_name

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if item in self.__devices:
            return self.__devices[item]

        if item in self.__services:
            return self.__services[item]

        if item in self.__class__.__dict__:
            if hasattr(self.__class__.__dict__[item], 'fget'):
                return self.__class__.__dict__[item].fget(self)

        raise AttributeError(item)


    def _get_parent_name(self):
        return 'UPNPObject'


    @property
    def services(self):
        return list(self.__services.values())[:]

    @property
    def devices(self):
        return list(self.__devices.values())[:]

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


class UPNPDevice(object):

    def __init__(self, url, location=None, node=None, parent=None):
        self.__parent = parent
        self.__services = {}
        self.__devices = {}
        self.__icons = {}
        if node is None:
            response = requests.get(url + location)
            root = ElementTree.fromstring(response.content)
            node = root.find(xmlns.device_xmlns('device'))

        icons = node.find(xmlns.device_xmlns('iconList')) or []
        services = node.find(xmlns.device_xmlns('serviceList')) or []
        devices = node.find(xmlns.device_xmlns('deviceList')) or []

        self.__node = node

        for icon in icons:
            icon = Icon(self, url, icon)
            self.__icons[icon.__name__] = icon

        for service in services:
            scpdurl = service.find(xmlns.device_xmlns('SCPDURL')).text
            control_url = service.find(xmlns.device_xmlns('controlURL')).text
            service_id = service.find(xmlns.device_xmlns('serviceId')).text
            service_type = service.find(xmlns.device_xmlns('serviceType')).text
            if location is None:
                scpdurl = scpdurl.encode('utf-8')
            else:
                scpdurl = (
                    b'/' +
                    location[1:].split(b'/')[0] +
                    b'/' +
                    scpdurl.encode('utf-8')
                )

            service = Service(self, url, scpdurl, service_type, control_url)
            name = service_id.split(':')[-1]
            service.__name__ = name
            self.__services[name] = service

        for device in devices:
            device = UPNPDevice(url, node=device, parent=self)
            self.__devices[device.__name__] = device

        self.url = url
        self.__name__ = self.friendly_name.replace(' ', '_').replace('-', '')


    def __str__(self, indent='  '):
        icons = ''
        for icon in self.icons:
            icons += icon.__str__(indent=indent + '    ')

        services = ''
        for service in self.services:
            services += service.__str__(indent=indent + '    ')

        devices = ''
        for device in self.devices:
            devices += device.__str__(indent=indent + '    ')

        output = TEMPLATE.format(
            indent=indent,
            access_point=self._get_parent_name(),
            friendly_name=self.friendly_name,
            manufacturer=self.manufacturer,
            manufacturer_url=self.manufacturer_url,
            model_description=self.model_description,
            model_name=self.model_name,
            model_number=self.model_number,
            model_url=self.model_url,
            serial_number=self.serial_number,
            presentation_url=self.presentation_url,
            device_type=self.device_type,
            hardware_id=self.hardware_id,
            device_category=self.device_category,
            device_subcategory=self.device_subcategory,
            udn=self.udn,
            upc=self.upc,
        )


        if icons:
            output += indent + 'Icons:\n' + icons
        else:
            output += indent + 'Icons: None\n'


        if services:
            output += indent + 'Services:\n' + services
        else:
            output += indent + 'Services: None\n'



        if devices:
            output += indent + 'Devices:\n' + devices
        else:
            output += indent + 'Devices: None\n'


        return output

    def _get_parent_name(self):
        if self.__parent is not None:
            return self.__parent._get_parent_name() + '.' + self.__name__
        else:
            return self.__name__

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if item in self.__services:
            return self.__services[item]
        if item in self.__devices:
            return self.__devices[item]
        if item in self.__icons:
            return self.__icons[item]

        if item in self.__class__.__dict__:
            if hasattr(self.__class__.__dict__[item], 'fget'):
                return self.__class__.__dict__[item].fget(self)

        raise AttributeError(item)

    def __get_xml_text(self, tag):
        value = self.__node.find(xmlns.device_xmlns(tag))
        if value is not None:
            value = value.text

        return value

    @property
    def hardware_id(self):
        value = self.__node.find(xmlns.pnpx_xmlns('X_hardwareId'))
        if value is not None:
            value = value.text.replace('&amp;', '&')

        return value

    @property
    def device_category(self):
        value = self.__node.find(xmlns.pnpx_xmlns('X_deviceCategory'))
        if value is not None:
            value = value.text

        return value

    @property
    def device_subcategory(self):
        value = self.__node.find(xmlns.df_xmlns('X_deviceCategory'))
        if value is not None:
            value = value.text

        return value

    @property
    def icons(self):
        return list(self.__icons.values())[:]

    @property
    def devices(self):
        return list(self.__devices.values())[:]

    @property
    def services(self):
        return list(self.__services.values())[:]

    @property
    def device_type(self):
        return self.__get_xml_text('deviceType')

    @property
    def presentation_url(self):
        value = self.__get_xml_text('presentationURL')
        if value is not None:
            return self.url + value.encode('utf-8')

    @property
    def friendly_name(self):
        return self.__get_xml_text('friendlyName')


    @property
    def manufacturer(self):
        return self.__get_xml_text('manufacturer')

    @property
    def manufacturer_url(self):
        return self.__get_xml_text('manufacturerURL')

    @property
    def model_description(self):
        return self.__get_xml_text('modelDescription')

    @property
    def model_name(self):
        return self.__get_xml_text('modelName')

    @property
    def model_number(self):
        return self.__get_xml_text('modelNumber')

    @property
    def model_url(self):
        return self.__get_xml_text('modelURL')

    @property
    def serial_number(self):
        return self.__get_xml_text('serialNumber')

    @property
    def udn(self):
        return self.__get_xml_text('UDN')

    @property
    def upc(self):
        return self.__get_xml_text('UPC')


TEMPLATE = '''
{indent}{friendly_name}
{indent}{manufacturer}
{indent}Access point: {access_point}
{indent}========================================================
{indent}Manufacturer URL:     {manufacturer_url}
{indent}Model Description:    {model_description}
{indent}Model Name:           {model_name}
{indent}Model Number:         {model_number}
{indent}Model URL:            {model_url}
{indent}Serial Number:        {serial_number}
{indent}Device Type:          {device_type}
{indent}Hardware ID:          {hardware_id}
{indent}Device Category:      {device_category}
{indent}Device Subcategory:   {device_subcategory}
{indent}Presentation URL:     {presentation_url}
{indent}UDN:                  {udn}
{indent}UPC:                  {upc}
'''
