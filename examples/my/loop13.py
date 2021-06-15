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
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    Floodlight=net.addController(name='Floodlight',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6653)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch,protocols="OpenFlow13")
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch,protocols="OpenFlow13")
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch,protocols="OpenFlow13")
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch,protocols="OpenFlow13")

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, mac='00:00:00:00:00:01',ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, mac='00:00:00:00:00:02',ip='10.0.0.2', defaultRoute=None)

    info( '*** Add links\n')
    bw = 1 # Mb
    delay = 10 # ms

    config = {'bw':bw,'delay':delay} #bw=100 MB delay=20ms
    net.addLink(s1, s2,cls=TCLink,**config)
    net.addLink(s1, s3,cls=TCLink,**config)
    net.addLink(s3, s4,cls=TCLink,**config)
    net.addLink(s4, s2,cls=TCLink,**config)
    net.addLink(s3, s2,cls=TCLink,**config)
    net.addLink(s1, s4,cls=TCLink,**config)
    net.addLink(h1, s1,cls=TCLink,**config)
    net.addLink(h2, s4,cls=TCLink,**config)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([Floodlight])
    net.get('s2').start([Floodlight])
    net.get('s3').start([Floodlight])
    net.get('s4').start([Floodlight])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
