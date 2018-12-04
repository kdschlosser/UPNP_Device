
SEC_XMLNS = '{http://www.sec.co.kr/dlna}'
DEVICE_XMLNS = '{urn:schemas-upnp-org:device-1-0}'
ENVELOPE_XMLNS = 'http://schemas.xmlsoap.org/soap/envelope/'
SERVICE_XMLNS = '{urn:schemas-upnp-org:service-1-0}'
DLNA_XMLNS = '{urn:schemas-dlna-org:device-1-0}'
PNPX_XMLNS = '{http://schemas.microsoft.com/windows/pnpx/2005/11}'
DF_XMLNS = '{http://schemas.microsoft.com/windows/2008/09/devicefoundation}'

def response_xmlns(service, tag):
    return '{' + service + '}' + tag


def envelope_xmlns(tag):
    return '{' + ENVELOPE_XMLNS + '}' + tag


def service_xmlns(tag):
    return SERVICE_XMLNS + tag


def sec_xmlns(tag):
    return SEC_XMLNS + tag


def device_xmlns(tag):
    return DEVICE_XMLNS + tag


def dlna_xmlns(tag):
    return DLNA_XMLNS + tag


def pnpx_xmlns(tag):
    return PNPX_XMLNS + tag


def df_xmlns(tag):
    return DF_XMLNS + tag
