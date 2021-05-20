#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False)

    info( '*** Adding controller\n' )
    floodlight=net.addController(name='floodlight',
                      controller=RemoteController,
                      ip='localhost',
                      protocol='tcp',
                      port=6653)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host,  defaultRoute=None)
    h2 = net.addHost('h2', cls=Host,  defaultRoute=None)
    h3 = net.addHost('h3', cls=Host,  defaultRoute=None)
    h4 = net.addHost('h4', cls=Host,  defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(s1, s4)
    net.addLink(s4, s2)
    net.addLink(s3, s2)
    net.addLink(s1, s3)
    net.addLink(h3, s1)
    net.addLink(h4, s1)
    net.addLink(s2, h1)
    net.addLink(s2, h2)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([floodlight])
    net.get('s2').start([floodlight])
    net.get('s3').start([floodlight])
    net.get('s4').start([floodlight])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

