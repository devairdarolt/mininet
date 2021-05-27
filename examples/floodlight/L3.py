#!/usr/bin/python
import json

#import httplib
import http.client
import os
import subprocess
import time
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import RemoteController
from mininet.topo import Topo
from mininet.util import irange
from mininet.topo import SingleSwitchTopo

HOME_FOLDER = os.getenv('HOME')


def getControllerIP():
   
    return "10.20.20.128"

def rest_call(path, data, action):
    headers = {
        'Content-type': 'application/json',
        'Accept'      : 'application/json',
    }
    body = json.dumps(data)

    #conn = httplib.HTTPConnection(getControllerIP(), 8080)
    conn = http.client.HTTPConnection(getControllerIP(), 8080)
    conn.request(action, path, body, headers)
    response = conn.getresponse()

    ret = (response.status, response.reason, response.read())
    conn.close()
    return ret

def addVirtualGateway(name):
    data = {
        "gateway-name" : name,
        "gateway-mac" : "aa:bb:cc:dd:ee:ff"
    }
    ret = rest_call('/wm/routing/gateway', data, 'POST')
    return ret

def addInterfaceToGateway(name):
    data = {
        "interfaces" : [
            {
                "interface-name" : "interface-1",
                "interface-ip" : "10.0.0.1",
                "interface-mask" : "255.255.255.0"
            },
            {
                "interface-name" : "interface-2",
                "interface-ip" : "20.0.0.1",
                "interface-mask" : "255.255.255.0"
            }
        ]
    }
    print('\n\n/wm/routing/gateway/' + name, data, 'POST\n\n\n')
    ret = rest_call('/wm/routing/gateway/' + name, data, 'POST')
    return ret

def addSwitchToGateway(name):
    data = {
        "gateway-name" : name,
        "gateway-ip" : "127.0.0.1",
        "switches": [{"dpid": "00:00:00:00:00:00:00:01"}]
    }
    ret = rest_call('/wm/routing/gateway/' + name, data, 'POST')
    return ret

def configureDefaultGatewayForHost(host, defaultGatewayIP):
    host.cmd('route add default gw ' + defaultGatewayIP);

def enableL3Routing():
    data = {
        "enable" : "true"
    }
    ret = rest_call('/wm/routing/config', data, 'POST')
    return ret


def disableL3Routing():
    data = {
        "enable" : "false"
    }
    ret = rest_call('/wm/routing/config', data, 'POST')
    return ret


def startNetworkWithLinearTopo( hostCount ):
    global net
    topo = SingleSwitchTopo( 2 )
    net = Mininet(topo=topo, build=False)




    remote_ip = getControllerIP()
    info('** Adding Floodlight Controller\n')
    net.addController('c1', controller=RemoteController,
                      ip=remote_ip, port=6653)

    # Build the network
    net.build()
    net.start()
    # Start L3 Routing
    ret = enableL3Routing()
    print (ret)

    ret = addVirtualGateway('mininet-gateway-1')
    print (ret)

    ret = addInterfaceToGateway('mininet-gateway-1')
    # ret = updateInterfaceToGateway('mininet-gateway-1')   # Just for test if gateway interface update correctly
    print (ret)

    ret = addSwitchToGateway('mininet-gateway-1')
    print (ret)

    # Need to configure default gw for host
    host1 = net.getNodeByName('h1')
    host1.setMAC( '00:00:00:00:00:01')
    host1.setIP('10.0.0.10', prefixLen=24)
    
    defaultGatewayIP1 = "10.0.0.1"
    configureDefaultGatewayForHost(host1, defaultGatewayIP1)

    host2 = net.getNodeByName('h2')
    host2.setMAC( '00:00:00:00:00:02')
    host2.setIP('20.0.0.20', prefixLen=24)
    defaultGatewayIP2 = "20.0.0.1"
    configureDefaultGatewayForHost(host2, defaultGatewayIP2)

def clearGatewayInstance(name):
    data = {}
    ret = rest_call('/wm/routing/gateway/' + name, data, 'DELETE')
    return ret


def stopNetwork():
    if net is not None:
        info('** Tearing down network\n')
        clearGatewayInstance('mininet-gateway-1')
        net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    startNetworkWithLinearTopo(2)
    CLI(net)
    stopNetwork()

