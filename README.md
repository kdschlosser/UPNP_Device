# UPNP Device
Discovers UPNP devices on the network.

***ADDED COMMAND LINE INTERFACE***

This is an extremely simple script to use. It consists of 2 mechanisms
to discover devices.

one is discover() and the other is listen().
The listen still needs some work.

It supports Multiple NIC's with multiple networks (even on the same NIC)
Windows, OSX and Linux are supported. There is one thing that this package
has the ability to do on Windows only and that is to get the default gateway
associated with a network. If someone knows how to obtain this information
without reading files or using some for of subprocess or the similar
thing in the os module it would be a great help. I do not know if there is
a piece of clib where the gateway can be obtained.

The gateway IP is needed to discover a router. Routers do not typically respond
to a network broadcast discover packet it has to be specifically
directed at the router. And this does work on Windows.


There are 2 params for the discover one being the timeout and the
other being for setting the log level using one of the levels in the
logging module. I have found that 3 seconds is a good timeout.


If you want to explore the newly created UPNP object simply print it.

it will tell you everything you need to know. like what parameters are
to be passed to a function and what the data types of the params are.
the return value types. and if there is a list that has to be selected from.

Even tho there may be multiple UPNP devices that point to the same ip address
I have compacted everything into a single object. so basically the object
will contain UPNP services and UPNP embedded  devices. the embedded
devices can contain their own services. and also their own embedded
devices as well. and so on and so forth.

when you print the UPNP object you will notice some data that states "Access point"
this is what you would use to access that specific piece.

This package is Python 2.7+ compatible
It does require the six package as well as the requests package.


## Command line interface


```




usage: upnp_device [-h --help] [-v --verbose] [--dump DIRECTORY] [--timeout TIMEEOUT]
                   [--execute ACCESS_POINT [additional execute parameters [-h, --help]]]
                   [ip [ip ...]]


positional arguments:
  *optional* ip                 ip address you want to search for
```
Here is the descriptions for the arguments<br></br>

optional argument|description
-----------------|-----------
-h, --help|show this help message and exit
-v, --verbose|increase output verbosity
--dump DIRECTORY|Directory wher you want to save the original UPNP xml files
--timeout TIMEEOUT|Search timeout in seconds. Default is 5
--execute ACCESS_POINT|If you do not specify this switch you will see a printout. In that printout you will see lines that say Access Point. this is what you want to enter as a parameter for this switch. you will also need to add more command line switches and values for each of the parameters that need to be passed. so if you havee a parameter of InstanceID you would add the switch like this --InstanceID 0 if you want help that will list out the parameters specify -h or --help after --executable



Example print outs

* TV

```
    UN55D8000
    IP Address: 192.168.1.201
    ==============================================
    Services:
        Service name: AVTransport
        Service class: urn:schemas-upnp-org:service:AVTransport:1
        Access point: UPNPObject.AVTransport
        ----------------------------------------------
        Methods:
            Method name: GetPositionInfo
            Access point: UPNPObject.AVTransport.GetPositionInfo
            ----------------------------------------------
                Parameters:
                UPNP data type: A_ARG_TYPE_InstanceID
                Py data type: unsigned 32bit int

                Return Values:
                    UPNP data type: CurrentTrack
                    Py data type: unsigned 32bit int
                    Default: 0
                    Minimum: 0
                    Maximum: 4294967295
                    Step: 1


                    UPNP data type: CurrentTrackDuration
                    Py data type: str, unicode
                    Default: 00:00:00


                    UPNP data type: CurrentTrackMetaData
                    Py data type: str, unicode


                    UPNP data type: CurrentTrackURI
                    Py data type: str, unicode


                    UPNP data type: RelativeTimePosition
                    Py data type: str, unicode
                    Default: 00:00:00


                    UPNP data type: AbsoluteTimePosition
                    Py data type: str, unicode
                    Default: 00:00:00


                    UPNP data type: RelativeCounterPosition
                    Py data type: signed 32bit int
                    Default: 2147483647


                    UPNP data type: AbsoluteCounterPosition
                    Py data type: signed 32bit int
                    Default: 2147483647

            Method name: GetTransportInfo
            Access point: UPNPObject.AVTransport.GetTransportInfo
            ----------------------------------------------
                Parameters:
                UPNP data type: A_ARG_TYPE_InstanceID
                Py data type: unsigned 32bit int

                Return Values:
                    UPNP data type: TransportState
                    Py data type: str, unicode
                    Default: NO_MEDIA_PRESENT
                    Possible returned values:
                        STOPPED
                        PAUSED_PLAYBACK
                        PLAYING
                        TRANSITIONING
                        NO_MEDIA_PRESENT


                    UPNP data type: TransportStatus
                    Py data type: str, unicode
                    Default: OK
                    Possible returned values:
                        OK
                        ERROR_OCCURRED


                    UPNP data type: TransportPlaySpeed
                    Py data type: str, unicode
                    Default: 1

        Service name: ConnectionManager
        Service class: urn:schemas-upnp-org:service:ConnectionManager:1
        Access point: UPNPObject.ConnectionManager
        ----------------------------------------------
        Methods:
            Method name: PrepareForConnection
            Access point: UPNPObject.ConnectionManager.PrepareForConnection
            ----------------------------------------------
                Parameters:
                UPNP data type: A_ARG_TYPE_ProtocolInfo
                Py data type: str, unicode


                UPNP data type: A_ARG_TYPE_ConnectionManager
                Py data type: str, unicode


                UPNP data type: A_ARG_TYPE_ConnectionID
                Py data type: signed 32bit int
                Default: 0


                UPNP data type: A_ARG_TYPE_Direction
                Py data type: str, unicode
                Allowed values:
                    Input
                    Output

                Return Values:
                    UPNP data type: A_ARG_TYPE_ConnectionID
                    Py data type: signed 32bit int
                    Default: 0


                    UPNP data type: A_ARG_TYPE_AVTransportID
                    Py data type: signed 32bit int
                    Default: 0


                    UPNP data type: A_ARG_TYPE_RcsID
                    Py data type: signed 32bit int
                    Default: 0
        Service name: RenderingControl
        Service class: urn:schemas-upnp-org:service:RenderingControl:1
        Access point: UPNPObject.RenderingControl
        ----------------------------------------------
        Methods:
            Method name: GetMute
            Access point: UPNPObject.RenderingControl.GetMute
            ----------------------------------------------
                Parameters:
                UPNP data type: A_ARG_TYPE_InstanceID
                Py data type: unsigned 32bit int


                UPNP data type: A_ARG_TYPE_Channel
                Py data type: str, unicode
                Allowed values:
                    Master

                Return Values:
                    UPNP data type: Mute
                    Py data type: bool
                    Possible returned values: True/False


    Devices: None

```

* Router

```
    RT224_Dual_WAN_Gigabit_VPN_Router
    IP Address: 192.168.1.1
    ==============================================
    Services:
        Service name: dummy1
        Service class: urn:schemas-dummy-com:service:Dummy:1
        Access point: UPNPObject.dummy1
        ----------------------------------------------
        Methods:
            None
    Devices:

        WANDevice
        Linksys, LLC.
        Access point: UPNPObject.WANDevice
        ========================================================
        Manufacturer URL:     http://www.linksys.com
        Model Description:    WAN Device on Linux IGD
        Model Name:           Linux IGD
        Model Number:         1.00
        Model URL:            http://www.linksys.com
        Serial Number:        1.00
        Device Type:          urn:schemas-upnp-org:device:WANDevice:1
        Hardware ID:          None
        Device Category:      None
        Device Subcategory:   None
        Presentation URL:     None
        UDN:                  uuid:75802409-bccb-40e7-8e6c-fa095ecce13e
        UPC:                  Linux IGD
        Icons: None
        Services:
            Service name: WANCommonIFC1
            Service class: urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1
            Access point: UPNPObject.WANDevice.WANCommonIFC1
            ----------------------------------------------
            Methods:
                Method name: GetCommonLinkProperties
                Access point: UPNPObject.WANDevice.WANCommonIFC1.GetCommonLinkProperties
                ----------------------------------------------
                    Parameters: None

                    Return Values:
                        UPNP data type: WANAccessType
                        Py data type: str, unicode
                        Possible returned values:
                            DSL
                            POTS
                            Cable
                            Ethernet
                            Other


                        UPNP data type: Layer1UpstreamMaxBitRate
                        Py data type: unsigned 32bit int


                        UPNP data type: Layer1DownstreamMaxBitRate
                        Py data type: unsigned 32bit int


                        UPNP data type: PhysicalLinkStatus
                        Py data type: str, unicode
                        Possible returned values:
                            Up
                            Down
                            Initializing
                            Unavailable


        Devices:

            WANConnectionDevice
            Linksys, LLC.
            Access point: UPNPObject.WANDevice.WANConnectionDevice
            ========================================================
            Manufacturer URL:     http://www.linksys.com
            Model Description:    WanConnectionDevice on Linux IGD
            Model Name:           Linux IGD
            Model Number:         0.95
            Model URL:            http://www.linksys.com
            Serial Number:        0.95
            Device Type:          urn:schemas-upnp-org:device:WANConnectionDevice:1
            Hardware ID:          None
            Device Category:      None
            Device Subcategory:   None
            Presentation URL:     None
            UDN:                  uuid:75802409-bccb-40e7-8e6c-fa095ecce13e
            UPC:                  Linux IGD
            Icons: None
            Services:
                Service name: WANIPConn1
                Service class: urn:schemas-upnp-org:service:WANIPConnection:1
                Access point: UPNPObject.WANDevice.WANConnectionDevice.WANIPConn1
                ----------------------------------------------
                Methods:
                    Method name: GetStatusInfo
                    Access point: UPNPObject.WANDevice.WANConnectionDevice.WANIPConn1.GetStatusInfo
                    ----------------------------------------------
                        Parameters: None

                        Return Values:
                            UPNP data type: ConnectionStatus
                            Py data type: str, unicode
                            Default: Unconfigured
                            Possible returned values:
                                Unconfigured
                                Connecting
                                Authenticating
                                PendingDisconnect
                                Disconnecting
                                Disconnected
                                Connected


                            UPNP data type: LastConnectionError
                            Py data type: str, unicode
                            Default: ERROR_NONE
                            Possible returned values:
                                ERROR_NONE
                                ERROR_ISP_TIME_OUT
                                ERROR_COMMAND_ABORTED
                                ERROR_NOT_ENABLED_FOR_INTERNET
                                ERROR_BAD_PHONE_NUMBER
                                ERROR_USER_DISCONNECT
                                ERROR_ISP_DISCONNECT
                                ERROR_IDLE_DISCONNECT
                                ERROR_FORCED_DISCONNECT
                                ERROR_SERVER_OUT_OF_RESOURCES
                                ERROR_RESTRICTED_LOGON_HOURS
                                ERROR_ACCOUNT_DISABLED
                                ERROR_ACCOUNT_EXPIRED
                                ERROR_PASSWORD_EXPIRED
                                ERROR_AUTHENTICATION_FAILURE
                                ERROR_NO_DIALTONE
                                ERROR_NO_CARRIER
                                ERROR_NO_ANSWER
                                ERROR_LINE_BUSY
                                ERROR_UNSUPPORTED_BITSPERSECOND
                                ERROR_TOO_MANY_LINE_ERRORS
                                ERROR_IP_CONFIGURATION
                                ERROR_UNKNOWN


                            UPNP data type: Uptime
                            Py data type: unsigned 32bit int
                            Default: 0
                            Minimum: 0
                            Step: 1


            Devices: None
```

you can also just get a printout of a specific device, service, or method
by simply printing that object
