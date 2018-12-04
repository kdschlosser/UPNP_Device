
import requests
from .xmlns import service_xmlns


class Action(object):

    def __init__(self, parent, node, state_variables, service, control_url):
        self.__parent = parent
        self.params = []
        self.ret_vals = []
        self.service = service
        self.control_url = control_url

        self.__name__ = node.find(service_xmlns('name')).text

        for arguments in node:
            if arguments.tag != service_xmlns('argumentList'):
                continue
            for argument in arguments:
                direction = argument.find(service_xmlns('direction')).text
                variable = argument.find(
                    service_xmlns('relatedStateVariable')
                ).text
                variable = state_variables[variable](direction)

                if direction == 'in':
                    self.params += [variable]
                else:
                    self.ret_vals += [variable]

    def __call__(self, *args, **kwargs):
        for i, arg in enumerate(args):
            try:
                kwargs[self.params[i].__name__] = arg
            except IndexError:
                for param in self.params:
                    print(param.__name__)
                raise

        doc = Document()

        envelope = doc.createElementNS('', 's:Envelope')
        envelope.setAttribute(
            'xmlns:s',
            ENVELOPE_XMLNS
        )
        envelope.setAttribute(
            's:encodingStyle',
            'http://schemas.xmlsoap.org/soap/encoding/'
        )

        body = doc.createElementNS('', 's:Body')

        fn = doc.createElementNS('', self.__name__)
        fn.setAttribute('xmlns:u', self.service)

        for param in self.params:
            if param.__name__ not in kwargs:
                value = param(None)
            else:
                value = param(kwargs[param.__name__])

            tmp_node = doc.createElement(param.__name__)
            tmp_text_node = doc.createTextNode(str(value))
            tmp_node.appendChild(tmp_text_node)
            fn.appendChild(tmp_node)

        body.appendChild(fn)
        envelope.appendChild(body)
        doc.appendChild(envelope)
        pure_xml = doc.toxml()

        header = {
            'SOAPAction':   '"{service}#{method}"'.format(
                service=self.service,
                method=self.__name__
            ),
            'Content-Type': 'text/xml'
        }

        response = requests.post(
            self.control_url,
            data=pure_xml,
            headers=header
        )

        envelope = ElementTree.fromstring(response.content)
        body = envelope.find(envelope_xmlns('Body'))

        return_value = []

        if body is not None:

            response = body.find(
                response_xmlns(self.service, self.__name__ + 'Response')
            )
            if response is not None:
                for ret_val in self.ret_vals:
                    value = response.find(ret_val.__name__)
                    if value is None:
                        value = ret_val(None)
                    else:
                        value = ret_val(value.text)

                    return_value += [value]

        if not return_value and self.ret_vals:
            for val in self.ret_vals:
                return_value += [val(None)]

        return return_value

    def _get_parent_name(self):
        return self.__parent._get_parent_name() + '.' + self.__name__

    def __str__(self, indent=''):
        if self.params:
            params = ''

            for param in self.params:
                params += param.__str__(indent + '    ') + '\n'
        else:
            params  = 'None\n\n'

        if self.ret_vals:
            ret_vals = ''

            for val in self.ret_vals:
                ret_vals += val.__str__(indent=indent + '        ') + '\n'

        else:
            ret_vals = 'None\n\n'

        output = TEMPLATE.format(
            indent=indent,
            name=self.__name__,
            access_point=self._get_parent_name(),
            params=params,
            ret_vals=ret_vals
        )

        return output


TEMPLATE = '''{indent}Method name: {name}
{indent}Access point: {access_point}
{indent}----------------------------------------------
{indent}    Parameters: {params}{indent}    Return Values: {ret_vals}'''
