import requests
from .xmlns import DEVICE_XMLNS


class Icon(object):

    def __init__(self, parent, url, node):
        self.__parent = parent
        self.mime_type = None
        self.width = None
        self.height = None
        self.depth = None
        self.url = None

        for item in node:
            tag = item.tag.replace(DEVICE_XMLNS, '')
            try:
                text = int(item.text)
            except ValueError:
                text = item.text

            if tag == 'url':
                name = text.split('/')[-1]
                name = name.replace('.', '_')
                self.__name__ = name
                text = url + text.encode('utf-8')

            setattr(self, tag, text)

    @property
    def data(self):
        return requests.get(self.url).content

    def _get_parent_name(self):
        return self.__parent._get_parent_name() + '.' + self.__name__

    def __str__(self, indent=''):
        output = TEMPLATE.format(
            indent=indent,
            access_point=self._get_parent_name(),
            name=self.__name__,
            mime_type=self.mime_type,
            width=self.width,
            height=self.height,
            depth=self.depth,
            url=self.url,
        )

        return output


TEMPLATE = '''
{indent}Icon name: {name}
{indent}Access point: {access_point}
{indent}----------------------------------------------
{indent}    Mime Type: {mime_type}
{indent}    Width: {width}
{indent}    Height: {height}
{indent}    Color Depth: {depth}
{indent}    URL: {url}
'''
