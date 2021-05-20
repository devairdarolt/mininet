#!/usr/bin/env python

import sys
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from mininet.log import lg, info
from mininet.topolib import TreeTopo
from mininet.util import waitListening

def connectToRootNS( network, switch, ip, routes ):
    """Connect hosts to root namespace via switch. Starts network.
      network: Mininet() network object
      switch: switch to connect to root namespace
      ip: IP address for root namespace node
      routes: host networks to route to"""
    # Create a node in root namespace and link to switch 0
    root = Node( 'root', inNamespace=False )
    intf = network.addLink( root, switch ).intf1
    root.setIP( ip, intf=intf )
    # Start network that now includes link to root namespace
    network.start()
    # Add routes from root ns to hosts
    for route in routes:
        root.cmd( 'route add -net ' + route + ' dev ' + str( intf ) )

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    floodlight=net.addController(name='floodlight',
                      controller=RemoteController,
                      ip='192.168.1.216',
                      protocol='tcp',
                      port=6653)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    

    info( '*** Add links\n')
    s1h1 = {'bw':100,'delay':'20'}
    net.addLink(s1, h1, cls=TCLink , **s1h1)

    s1h2 = {'bw':100,'delay':'20'}
    net.addLink(s1, h2, cls=TCLink , **s1h2)

    s1h3 = {'bw':100,'delay':'20'}
    net.addLink(s1, h3, cls=TCLink , **s1h3)

    s1h4 = {'bw':100,'delay':'20'}
    net.addLink(s1, h4, cls=TCLink , **s1h4)
    

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([floodlight])

    info( '*** Post configure switches and hosts\n')



    argvopts = ' '.join( sys.argv[ 1: ] ) if len( sys.argv ) > 1 else (
        '-D -o UseDNS=no -u0' )

    
    switch = s1

    opts='-D'
    cmd='/usr/sbin/sshd'
    ip='10.123.123.1/32'
    routes = [ '10.0.0.0/24' ]
    connectToRootNS( net, switch, ip, routes )

    for host in net.hosts:
        host.cmd( cmd + ' ' + opts + '&' )
    info( "*** Waiting for ssh daemons to start\n" )
    for server in net.hosts:
        waitListening( server=server, port=22, timeout=5 )

    info( "\n*** Hosts are running sshd at the following addresses:\n" )
    for host in net.hosts:
        info( host.name, host.IP(), '\n' )
    info( "\n*** Type 'exit' or control-D to shut down network\n" )




    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

