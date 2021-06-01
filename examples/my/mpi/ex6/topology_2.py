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
import os
from mininet.util import waitListening
from mininet.clean import cleanup
import re

def macAddressToDecimal(mac):
    res = re.match('^((?:(?:[0-9a-f]{2}):){5}[0-9a-f]{2})$', mac.lower())
    if res is None:
        raise ValueError('invalid mac address')
    return int(res.group(0).replace(':', ''), 16)

def decimalToMacAddress(macint):
    if type(macint) != int:
        raise ValueError('invalid integer')
    return ':'.join(['{}{}'.format(a, b)
                     for a, b
                     in zip(*[iter('{:012x}'.format(macint))]*2)])

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
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, dpid='1',protocols="OpenFlow13")
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, dpid='2',protocols="OpenFlow13")
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, dpid='3',protocols="OpenFlow13")
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch, dpid='4',protocols="OpenFlow13")
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch, dpid='5',protocols="OpenFlow13")
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch, dpid='6',protocols="OpenFlow13")
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch, dpid='7',protocols="OpenFlow13")
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch, dpid='8',protocols="OpenFlow13")
    s11 = net.addSwitch('s11', cls=OVSKernelSwitch, dpid='11',protocols="OpenFlow13")
    s12 = net.addSwitch('s12', cls=OVSKernelSwitch, dpid='12',protocols="OpenFlow13")
    s13 = net.addSwitch('s13', cls=OVSKernelSwitch, dpid='13',protocols="OpenFlow13")
    s14 = net.addSwitch('s14', cls=OVSKernelSwitch, dpid='14',protocols="OpenFlow13")
    s15 = net.addSwitch('s15', cls=OVSKernelSwitch, dpid='15',protocols="OpenFlow13")
    s16 = net.addSwitch('s16', cls=OVSKernelSwitch, dpid='16',protocols="OpenFlow13")
    s17 = net.addSwitch('s17', cls=OVSKernelSwitch, dpid='17',protocols="OpenFlow13")
    s18 = net.addSwitch('s18', cls=OVSKernelSwitch, dpid='18',protocols="OpenFlow13")
    s21 = net.addSwitch('s21', cls=OVSKernelSwitch, dpid='21',protocols="OpenFlow13")
    s22 = net.addSwitch('s22', cls=OVSKernelSwitch, dpid='22',protocols="OpenFlow13")
    s23 = net.addSwitch('s23', cls=OVSKernelSwitch, dpid='23',protocols="OpenFlow13")
    s24 = net.addSwitch('s24', cls=OVSKernelSwitch, dpid='24',protocols="OpenFlow13")

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None, mac=decimalToMacAddress(1))
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None, mac=decimalToMacAddress(2))
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None, mac=decimalToMacAddress(3))
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None, mac=decimalToMacAddress(4))
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None, mac=decimalToMacAddress(5))
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None, mac=decimalToMacAddress(6))
    h7 = net.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None, mac=decimalToMacAddress(7))
    h8 = net.addHost('h8', cls=Host, ip='10.0.0.8', defaultRoute=None, mac=decimalToMacAddress(8))
    h9 = net.addHost('h9', cls=Host, ip='10.0.0.9', defaultRoute=None, mac=decimalToMacAddress(9))
    h10 = net.addHost('h10', cls=Host, ip='10.0.0.10', defaultRoute=None, mac=decimalToMacAddress(10))
    h11 = net.addHost('h11', cls=Host, ip='10.0.0.11', defaultRoute=None, mac=decimalToMacAddress(11))
    h12 = net.addHost('h12', cls=Host, ip='10.0.0.12', defaultRoute=None, mac=decimalToMacAddress(12))
    h13 = net.addHost('h13', cls=Host, ip='10.0.0.13', defaultRoute=None, mac=decimalToMacAddress(13))
    h14 = net.addHost('h14', cls=Host, ip='10.0.0.14', defaultRoute=None, mac=decimalToMacAddress(14))
    h15 = net.addHost('h15', cls=Host, ip='10.0.0.15', defaultRoute=None, mac=decimalToMacAddress(15))
    h16 = net.addHost('h16', cls=Host, ip='10.0.0.16', defaultRoute=None, mac=decimalToMacAddress(16))

    info( '*** Add links\n')
    h1s1 = {'bw':50,'delay':'20'}
    net.addLink(h1, s1, cls=TCLink , **h1s1)
    h2s1 = {'bw':50,'delay':'20'}
    net.addLink(h2, s1, cls=TCLink , **h2s1)
    h3s2 = {'bw':50,'delay':'20'}
    net.addLink(h3, s2, cls=TCLink , **h3s2)
    h4s2 = {'bw':50,'delay':'20'}
    net.addLink(h4, s2, cls=TCLink , **h4s2)
    h5s3 = {'bw':50,'delay':'20'}
    net.addLink(h5, s3, cls=TCLink , **h5s3)
    h6s3 = {'bw':50,'delay':'20'}
    net.addLink(h6, s3, cls=TCLink , **h6s3)
    h7s4 = {'bw':50,'delay':'20'}
    net.addLink(h7, s4, cls=TCLink , **h7s4)
    h8s4 = {'bw':50,'delay':'20'}
    net.addLink(h8, s4, cls=TCLink , **h8s4)
    h9s5 = {'bw':50,'delay':'20'}
    net.addLink(h9, s5, cls=TCLink , **h9s5)
    h10s5 = {'bw':50,'delay':'20'}
    net.addLink(h10, s5, cls=TCLink , **h10s5)
    h11s6 = {'bw':50,'delay':'20'}
    net.addLink(h11, s6, cls=TCLink , **h11s6)
    h12s6 = {'bw':50,'delay':'20'}
    net.addLink(h12, s6, cls=TCLink , **h12s6)
    h13s7 = {'bw':50,'delay':'20'}
    net.addLink(h13, s7, cls=TCLink , **h13s7)
    h14s7 = {'bw':50,'delay':'20'}
    net.addLink(h14, s7, cls=TCLink , **h14s7)
    h15s8 = {'bw':50,'delay':'20'}
    net.addLink(h15, s8, cls=TCLink , **h15s8)
    h16s8 = {'bw':50,'delay':'20'}
    net.addLink(h16, s8, cls=TCLink , **h16s8)
    s21s11 = {'bw':1000,'delay':'5'}
    net.addLink(s21, s11, cls=TCLink , **s21s11)
    s21s13 = {'bw':1000,'delay':'5'}
    net.addLink(s21, s13, cls=TCLink , **s21s13)
    s21s15 = {'bw':1000,'delay':'5'}
    net.addLink(s21, s15, cls=TCLink , **s21s15)
    s21s17 = {'bw':1000,'delay':'5'}
    net.addLink(s21, s17, cls=TCLink , **s21s17)
    s22s11 = {'bw':1000,'delay':'5'}
    net.addLink(s22, s11, cls=TCLink , **s22s11)
    s22s13 = {'bw':1000,'delay':'5'}
    net.addLink(s22, s13, cls=TCLink , **s22s13)
    s22s15 = {'bw':1000,'delay':'5'}
    net.addLink(s22, s15, cls=TCLink , **s22s15)
    s22s17 = {'bw':1000,'delay':'5'}
    net.addLink(s22, s17, cls=TCLink , **s22s17)
    s12s23 = {'bw':1000,'delay':'5'}
    net.addLink(s12, s23, cls=TCLink , **s12s23)
    s14s23 = {'bw':1000,'delay':'5'}
    net.addLink(s14, s23, cls=TCLink , **s14s23)
    s16s23 = {'bw':1000,'delay':'5'}
    net.addLink(s16, s23, cls=TCLink , **s16s23)
    s18s23 = {'bw':1000,'delay':'5'}
    net.addLink(s18, s23, cls=TCLink , **s18s23)
    s12s24 = {'bw':1000,'delay':'5'}
    net.addLink(s12, s24, cls=TCLink , **s12s24)
    s14s24 = {'bw':1000,'delay':'5'}
    net.addLink(s14, s24, cls=TCLink , **s14s24)
    s16s24 = {'bw':1000,'delay':'5'}
    net.addLink(s16, s24, cls=TCLink , **s16s24)
    s18s24 = {'bw':1000,'delay':'5'}
    net.addLink(s18, s24, cls=TCLink , **s18s24)
    s11s1 = {'bw':100,'delay':'10'}
    net.addLink(s11, s1, cls=TCLink , **s11s1)
    s11s2 = {'bw':100,'delay':'10'}
    net.addLink(s11, s2, cls=TCLink , **s11s2)
    s12s1 = {'bw':100,'delay':'10'}
    net.addLink(s12, s1, cls=TCLink , **s12s1)
    s12s2 = {'bw':100,'delay':'10'}
    net.addLink(s12, s2, cls=TCLink , **s12s2)
    s13s3 = {'bw':100,'delay':'10'}
    net.addLink(s13, s3, cls=TCLink , **s13s3)
    s13s4 = {'bw':100,'delay':'10'}
    net.addLink(s13, s4, cls=TCLink , **s13s4)
    s14s3 = {'bw':100,'delay':'10'}
    net.addLink(s14, s3, cls=TCLink , **s14s3)
    s14s4 = {'bw':100,'delay':'10'}
    net.addLink(s14, s4, cls=TCLink , **s14s4)
    s15s5 = {'bw':100,'delay':'10'}
    net.addLink(s15, s5, cls=TCLink , **s15s5)
    s15s6 = {'bw':100,'delay':'10'}
    net.addLink(s15, s6, cls=TCLink , **s15s6)
    s16s5 = {'bw':100,'delay':'10'}
    net.addLink(s16, s5, cls=TCLink , **s16s5)
    s16s6 = {'bw':100,'delay':'10'}
    net.addLink(s16, s6, cls=TCLink , **s16s6)
    s17s7 = {'bw':100,'delay':'10'}
    net.addLink(s17, s7, cls=TCLink , **s17s7)
    s17s8 = {'bw':100,'delay':'10'}
    net.addLink(s17, s8, cls=TCLink , **s17s8)
    s18s7 = {'bw':100,'delay':'10'}
    net.addLink(s18, s7, cls=TCLink , **s18s7)
    s18s8 = {'bw':100,'delay':'10'}
    net.addLink(s18, s8, cls=TCLink , **s18s8)

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
    net.get('s5').start([Floodlight])
    net.get('s6').start([Floodlight])
    net.get('s7').start([Floodlight])
    net.get('s8').start([Floodlight])
    net.get('s11').start([Floodlight])
    net.get('s12').start([Floodlight])
    net.get('s13').start([Floodlight])
    net.get('s14').start([Floodlight])
    net.get('s15').start([Floodlight])
    net.get('s16').start([Floodlight])
    net.get('s17').start([Floodlight])
    net.get('s18').start([Floodlight])
    net.get('s21').start([Floodlight])
    net.get('s22').start([Floodlight])
    net.get('s23').start([Floodlight])
    net.get('s24').start([Floodlight])

    info( '*** Post configure switches and hosts\n')
    
    os.system("useradd mininet_user")
    


    info( '*** ssh init\n')
    for host in net.hosts:
        
        host.cmd("/usr/sbin/sshd -o UseDNS=no -u0 &")
        host.cmd("xterm -e ssh -X mininet_user@localhost &")


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
        os.system("kill -9 $(pgrep -f xterm)")

        os.system("userdel mininet_user")
    

