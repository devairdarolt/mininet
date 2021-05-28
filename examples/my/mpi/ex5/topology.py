#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
import os
from mininet.util import waitListening
from mininet.clean import cleanup

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    Floodlight=net.addController(name='Floodlight',
                      controller=RemoteController,
                      ip='10.20.221.81',
                      protocol='tcp',
                      port=6653)

    # POD 1
    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None)
    #h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    net.addLink(s2, h3)
    net.addLink(s2, h4)
    net.addLink(s3, s1)
    net.addLink(s4, s2)
    net.addLink(s3, s2)
    net.addLink(s4, s1)
    net.addLink(s5, s3)
    net.addLink(s5, s4)
    #net.addLink(h5, s5)


    # POD 2
    info( '*** Add switches\n')
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch)
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch)
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch)
    s9 = net.addSwitch('s9', cls=OVSKernelSwitch)
    s10 = net.addSwitch('s10', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None)
    h7 = net.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None)
    h8 = net.addHost('h8', cls=Host, ip='10.0.0.8', defaultRoute=None)
    h9 = net.addHost('h9', cls=Host, ip='10.0.0.9', defaultRoute=None)
    #h10 = net.addHost('h10', cls=Host, ip='10.0.0.10', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(s6, h6)
    net.addLink(s6, h7)
    net.addLink(s7, h8)
    net.addLink(s7, h9)
    net.addLink(s8, s6)
    net.addLink(s9, s7)
    net.addLink(s8, s7)
    net.addLink(s9, s6)
    net.addLink(s10, s8)
    net.addLink(s10, s9)
    #net.addLink(h10, s10)


    #core
    net.addLink(s10, s5)


    info( '*** Starting network\n')
    net.build()

    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()


    info( '*** Starting sshd\n')
    for host in net.hosts:
        host.cmd('/usr/sbin/sshd -D &')

    #check if port is listening
    #for host in net.hosts:
    #    waitListening( client=None, server=host.IP(), port=22, timeout=5 )
        

    info( "\n*** Hosts are running sshd at the following addresses:\n" )
    for host in net.hosts:
        info( host.name, host.IP(), '\n' )
    info( "\n*** Type 'exit' or control-D to shut down network\n" )

    info( '*** Starting switches\n')
    net.get('s1').start([Floodlight])
    net.get('s2').start([Floodlight])
    net.get('s3').start([Floodlight])
    net.get('s4').start([Floodlight])
    net.get('s5').start([Floodlight])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    try:
        setLogLevel( 'info' )
        myNetwork()
    except:
        print("Error on start. mn -c")
    
    finally:
        cleanup()
        print("kill sshd listeners\nkill -9 $(pgrep -f listener)")
        os.system("kill -9 $(pgrep -f listener)")
        

