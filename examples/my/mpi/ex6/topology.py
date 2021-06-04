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
import re


#ip='10.20.221.81'

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

def fattree():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller Floodlight ***\n' )
    Floodlight=net.addController(name='Floodlight',
                      controller=RemoteController,
                      ip='localhost',
                      protocol='tcp',
                      port=6653)

    k = 4 # Número de portas/switches
    khosts = 16 # Hosts
    
    #computador = net.addHost("computador",hostname="computador",cls=Host, ip="10.0.0.100", mac="aa:bb:cc:dd:ee:ff",defaultRoute=None)
        
    info( '*** Creating hosts ***\n')
    for i in range(1,khosts+1):
        hostname = "h%s"%i
        ip = "10.0.0.%s"%i
        mac=decimalToMacAddress(i)
        host = net.addHost("h%s"%i,hostname=hostname,cls=Host, ip=ip, mac=mac,defaultRoute=None)        
        info(host,"\t", ip,"\t", mac,"\n")
                        

    info( '*** Creating roots switches ***\n')
    for i in range(1,k+1):
        sw = net.addSwitch('s2%s'%i, cls=OVSKernelSwitch,protocols="OpenFlow13")
        print(sw)
    

    info( '*** Creating aggs switches ***\n')
    for i in range(1,2*k+1):
        sw = net.addSwitch('s1%s'%i, cls=OVSKernelSwitch,protocols="OpenFlow13")
        print(sw)

    info( '*** Creating edges switches ***\n')
    for i in range(1,2*k+1):
        sw = net.addSwitch('s%s'%i, cls=OVSKernelSwitch,protocols="OpenFlow13")
        print(sw)


    info( '*** Creating lisks hosts-edges ***\n')
    edge_host_bw = 1 # Mb
    edge_host_delay = 10 # ms
    s1h1 = {'bw':edge_host_bw,'delay':edge_host_delay} #bw=100 MB delay=20ms
    net.addLink(net.get('s1'),net.get('h1'), port1=3, port2= 0,cls=TCLink,**s1h1)
    
    s1h2 = {'bw':edge_host_bw,'delay':edge_host_delay} #bw=100 MB delay=20ms
    net.addLink(net.get('s1'),net.get('h2'), port1=4, port2= 0,cls=TCLink,**s1h2)

    s2h3 = {'bw':edge_host_bw,'delay':edge_host_delay} #bw=100 MB delay=20ms
    net.addLink(net.get('s2'),net.get('h3'), port1=3, port2= 0,cls=TCLink,**s2h3)

    s2h4 = {'bw':edge_host_bw,'delay':edge_host_delay} #bw=100 MB delay=20ms
    net.addLink(net.get('s2'),net.get('h4'), port1=4, port2= 0,cls=TCLink,**s2h4)

    s3h5 = {'bw':edge_host_bw,'delay':edge_host_delay} #bw=100 MB delay=20ms
    net.addLink(net.get('s3'),net.get('h5'), port1=3, port2= 0,cls=TCLink,**s3h5)

    s3h6 = {'bw':edge_host_bw,'delay':edge_host_delay} #bw=100 MB delay=20ms
    net.addLink(net.get('s3'),net.get('h6'), port1=4, port2= 0,cls=TCLink,**s3h6)

    s4h7 = {'bw':edge_host_bw,'delay':edge_host_delay} #bw=100 MB delay=20ms
    net.addLink(net.get('s4'),net.get('h7'), port1=3, port2= 0,cls=TCLink,**s4h7)    

    s4h8 = {'bw':edge_host_bw,'delay':edge_host_delay} #bw=100 MB delay=20ms
    net.addLink(net.get('s4'),net.get('h8'), port1=4, port2= 0,cls=TCLink,**s4h8)

    s5h9 = {'bw':edge_host_bw,'delay':edge_host_delay} #bw=100 MB delay=20ms
    net.addLink(net.get('s5'),net.get('h9'), port1=3, port2= 0,cls=TCLink,**s5h9)

    s5h10 = {'bw':edge_host_bw,'delay':edge_host_delay} #bw=100 MB delay=20ms
    net.addLink(net.get('s5'),net.get('h10'), port1=4, port2= 0,cls=TCLink,**s5h10)

    s6h11 = {'bw':edge_host_bw,'delay':edge_host_delay} #bw=100 MB delay=20ms
    net.addLink(net.get('s6'),net.get('h11'), port1=3, port2= 0,cls=TCLink,**s6h11)

    s6h12 = {'bw':edge_host_bw,'delay':edge_host_delay} #bw=100 MB delay=20ms
    net.addLink(net.get('s6'),net.get('h12'), port1=4, port2= 0,cls=TCLink,**s6h12)

    s7h13 = {'bw':edge_host_bw,'delay':edge_host_delay} #bw=100 MB delay=20ms
    net.addLink(net.get('s7'),net.get('h13'), port1=3, port2= 0,cls=TCLink,**s7h13)

    s7h14 = {'bw':edge_host_bw,'delay':edge_host_delay} #bw=100 MB delay=20ms
    net.addLink(net.get('s7'),net.get('h14'), port1=4, port2= 0,cls=TCLink,**s7h14) 

    s8h15 = {'bw':edge_host_bw,'delay':edge_host_delay} #bw=100 MB delay=20ms
    net.addLink(net.get('s8'),net.get('h15'), port1=3, port2= 0,cls=TCLink,**s8h15)

    s8h16 = {'bw':edge_host_bw,'delay':edge_host_delay} #bw=100 MB delay=20ms
    net.addLink(net.get('s8'),net.get('h16'), port1=4, port2= 0,cls=TCLink,**s8h16)
    

    '''s21computador = {'bw':edge_host_bw,'delay':edge_host_delay} #bw=100 MB delay=20ms
    net.addLink(net.get('s21'),computador, port1=4, port2= 0,cls=TCLink,**s21computador)'''

    info( '\n*** Starting network ***\n')


    info( '\n*** Creating lisks aggs-edges ***\n')

    agg_edge_bw = 100   # 100 Mb
    agg_edge_delay = 10 # 10 ms

    s11s1 = {'bw':agg_edge_bw,'delay':agg_edge_delay} #bw=100 MB delay=10ms
    net.addLink(net.get('s11'),net.get('s1'), port1=3, port2=1 ,cls=TCLink,**s11s1)

    s11s2 = {'bw':agg_edge_bw,'delay':agg_edge_delay} #bw=100 MB delay=10ms
    net.addLink(net.get('s11'),net.get('s2'), port1=4, port2=1 ,cls=TCLink,**s11s2)

    '''
    s12s1 = {'bw':agg_edge_bw,'delay':agg_edge_delay} #bw=100 MB delay=10ms
    net.addLink(net.get('s12'),net.get('s1'), port1=3, port2=2 ,cls=TCLink,**s12s1)

    s12s2 = {'bw':agg_edge_bw,'delay':agg_edge_delay} #bw=100 MB delay=10ms
    net.addLink(net.get('s12'),net.get('s2'), port1=4, port2=2 ,cls=TCLink,**s12s2)

    s13s3 = {'bw':agg_edge_bw,'delay':agg_edge_delay} #bw=100 MB delay=10ms
    net.addLink(net.get('s13'),net.get('s3'), port1=3, port2=1 ,cls=TCLink,**s13s3)

    s13s4 = {'bw':agg_edge_bw,'delay':agg_edge_delay} #bw=100 MB delay=10ms
    net.addLink(net.get('s13'),net.get('s4'), port1=4, port2=1 ,cls=TCLink,**s13s4)

    s14s3 = {'bw':agg_edge_bw,'delay':agg_edge_delay} #bw=100 MB delay=10ms
    net.addLink(net.get('s14'),net.get('s3'), port1=3, port2=2 ,cls=TCLink,**s14s3)

    s14s4 = {'bw':agg_edge_bw,'delay':agg_edge_delay} #bw=100 MB delay=10ms
    net.addLink(net.get('s14'),net.get('s4'), port1=4, port2=2 ,cls=TCLink,**s14s4)

    s15s5 = {'bw':agg_edge_bw,'delay':agg_edge_delay} #bw=100 MB delay=10ms
    net.addLink(net.get('s15'),net.get('s5'), port1=3, port2=1 ,cls=TCLink,**s15s5)

    s15s6 = {'bw':agg_edge_bw,'delay':agg_edge_delay} #bw=100 MB delay=10ms
    net.addLink(net.get('s15'),net.get('s6'), port1=4, port2= 1,cls=TCLink,**s15s6)

    s16s5 = {'bw':agg_edge_bw,'delay':agg_edge_delay} #bw=100 MB delay=10ms
    net.addLink(net.get('s16'),net.get('s5'), port1=3, port2= 2,cls=TCLink,**s16s5)

    s16s6 = {'bw':agg_edge_bw,'delay':agg_edge_delay} #bw=100 MB delay=10ms
    net.addLink(net.get('s16'),net.get('s6'), port1=4, port2= 2,cls=TCLink,**s16s6)
    
    s17s7 = {'bw':agg_edge_bw,'delay':agg_edge_delay} #bw=100 MB delay=10ms
    net.addLink(net.get('s17'),net.get('s7'), port1=3, port2= 1,cls=TCLink,**s17s7)

    s17s8 = {'bw':agg_edge_bw,'delay':agg_edge_delay} #bw=100 MB delay=10ms
    net.addLink(net.get('s17'),net.get('s8'), port1=4, port2= 1,cls=TCLink,**s17s8)

    s18s7 = {'bw':agg_edge_bw,'delay':agg_edge_delay} #bw=100 MB delay=10ms
    net.addLink(net.get('s18'),net.get('s7'), port1=3, port2= 2,cls=TCLink,**s18s7)

    s18s8 = {'bw':agg_edge_bw,'delay':agg_edge_delay} #bw=100 MB delay=10ms
    net.addLink(net.get('s18'),net.get('s8'), port1=4, port2= 2,cls=TCLink,**s18s8)'''



    net.build()

    '''##Forech host -> create a user, and auto login ssh
    cmd = "/usr/sbin/sshd -o UseDNS=no -u0 &"
    computador.cmd(cmd)    
    computador.cmd("xterm -e ssh -X devairdarolt@localhost")'''




    info( "\n*** Hosts are running sshd at the following addresses:\n" )
    for host in net.hosts:
        info( host.name, host.IP(), '\n' )

    info( '\n*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( "\n*** Init edge switch in Floodlight\n" )
    for i in range (1,2*k+1):
        net.get('s%s'%i).start([Floodlight])


    CLI(net)
    net.stop()

if __name__ == '__main__':
    try:
        setLogLevel( 'info' )
        fattree()
    except:
        print("Error on start. mn -c")
    
    finally:
        cleanup()
        print("kill sshd listeners\nkill -9 $(pgrep -f listener)")
        os.system("kill -9 $(pgrep -f listener)")
        

