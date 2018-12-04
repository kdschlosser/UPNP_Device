
import requests
from xml.etree import cElementTree as ElementTree
from .xmlns import service_xmlns, device_xmlns, pnpx_xmlns, df_xmlns
from .data_type import StateVariable
from .action import Action
from .icon import Icon


class Service(object):

    def __init__(
        self,
        parent,
        url,
        location,
        service,
        control_url,
        node=None
    ):

        self.__parent = parent
        self.state_variables = {}
        self.actions = {}
        self.__node = node
        self.url = url
        self.__icons = {}

        if node is not None:
            icons = node.find(device_xmlns('iconList')) or []

            for icon in icons:
                icon = Icon(self, url, icon)
                self.__icons[icon.__name__] = icon


        self.service = service
        response = requests.get(url + location)
        root = ElementTree.fromstring(response.content)

        actions = root.find(service_xmlns('actionList')) or []
        state_variables = root.find(service_xmlns('serviceStateTable')) or []
        for state_variable in state_variables:
            state_variable = StateVariable(state_variable)
            self.state_variables[state_variable.name] = state_variable

        for action in actions:
            try:
                action = Action(
                    self,
                    action,
                    self.state_variables,
                    service,
                    url.decode('utf-8') + control_url
                )
            except AttributeError:
                action = Action(
                    self,
                    action,
                    self.state_variables,
                    service,
                    url + control_url
                )
            self.actions[action.__name__] = action

    def _get_parent_name(self):
        return self.__parent._get_parent_name() + '.' + self.__name__

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if item in self.actions:
            return self.actions[item]

        if self.__node is not None:
            if item in self.__icons:
                return self.__icons[item]

            if item in self.__class__.__dict__:
                if hasattr(self.__class__.__dict__[item], 'fget'):
                    return self.__class__.__dict__[item].fget(self)

        raise AttributeError(item)

    def __str__(self, indent=''):
        actions = ''

        for action in self.actions.values():
            actions += action.__str__(indent + '    ')

        if not actions:
            actions += indent + '    None'

        if self.__node is None:

            output = TEMPLATE.format(
                indent=indent,
                access_point=self._get_parent_name(),
                service=self.service,
                name=self.__name__,
                actions=actions
            )
            return output

        icons = ''
        for icon in self.icons:
            icons += icon.__str__(indent=indent + '    ') + '\n'

        if not icons:
            icons = indent + '    None'

        output = TEMPLATE.format(
            indent=indent,
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
            icons=icons,
            access_point=self._get_parent_name(),
            service=self.service,
            name=self.__name__,
            actions=actions.rstrip() + '\n'
        )

        return output

    def __get_xml_text(self, tag):
        value = self.__node.find(device_xmlns(tag))
        if value is not None:
            value = value.text

        return value

    @property
    def hardware_id(self):
        value = self.__node.find(pnpx_xmlns('X_hardwareId'))
        if value is not None:
            value = value.text.replace('&amp;', '&')

        return value

    @property
    def device_category(self):
        value = self.__node.find(pnpx_xmlns('X_deviceCategory'))
        if value is not None:
            value = value.text

        return value

    @property
    def device_subcategory(self):
        value = self.__node.find(df_xmlns('X_deviceCategory'))
        if value is not None:
            value = value.text

        return value

    @property
    def icons(self):
        return list(self.__icons.values())[:]

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


TEMPLATE = '''{indent}Service name: {name}
{indent}Service class: {service}
{indent}Access point: {access_point}
{indent}----------------------------------------------
{indent}Methods:
{actions}
'''

TEMPLATE2 = '''{indent}Service name: {name}
{indent}Service class: {service}
{indent}Access point: {access_point}
{indent}----------------------------------------------
{indent}Manufacturer:         {manufacturer}
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
{indent}--------------------------------------------------------
{indent}Icons
{indent}--------------------------------------------------------
{icons}
{indent}Methods:
{actions}
'''
