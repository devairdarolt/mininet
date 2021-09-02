#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import OVSKernelSwitch
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf, TCLink
from mininet.topo import Topo
from mininet.util import dumpNodeConnections
from subprocess import call
import logging
import os
from mininet.util import waitListening
from mininet.clean import cleanup
import re

#logging.basicConfig(filename='./fattree.log', level=logging.INFO)
#logger = logging.getLogger(__name__)


class Fattree(Topo):
    CoreSwitchList = []
    AggSwitchList = []
    EdgeSwitchList = []
    HostList = []

    def __init__(self, k, density):
        self.pod = k
        self.iCoreLayerSwitch = (k/2)**2
        self.iAggLayerSwitch = k*k/2
        self.iEdgeLayerSwitch = k*k/2
        self.density = density
        self.iHost = self.iEdgeLayerSwitch * density

        #Init Topo
        Topo.__init__(self)

    def createTopo(self):
        self.createCoreLayerSwitch(self.iCoreLayerSwitch)
        self.createAggLayerSwitch(self.iAggLayerSwitch)
        self.createEdgeLayerSwitch(self.iEdgeLayerSwitch)
        self.createHost(self.iHost)

    """
    Create Switch and Host
    """

    def _addSwitch(self, number, level, switch_list):
        for x in range(1, int(number+1)):
            PREFIX = str(level) + "00"
            if x >= int(10):
                PREFIX = str(level) + "0"
            switch_list.append(self.addSwitch('s' + PREFIX + str(x),cls=OVSKernelSwitch,protocols="OpenFlow13"))

    def createCoreLayerSwitch(self, NUMBER):
        self._addSwitch(NUMBER, 1, self.CoreSwitchList)

    def createAggLayerSwitch(self, NUMBER):
        self._addSwitch(NUMBER, 2, self.AggSwitchList)

    def createEdgeLayerSwitch(self, NUMBER):
        self._addSwitch(NUMBER, 3, self.EdgeSwitchList)

    def createHost(self, NUMBER):
        for x in range(1, int(NUMBER+1)):
            PREFIX = "h00"
            if x >= int(10):
                PREFIX = "h0"
            elif x >= int(100):
                PREFIX = "h"
            self.HostList.append(self.addHost(PREFIX + str(x)))

    """
    Add Link
    """
    def createLink(self, bw_c2a=0.2, bw_a2e=0.1, bw_h2e=0.5):
        end = int(self.pod/2)
        for x in range(0, int(self.iAggLayerSwitch), int(end)):
            for i in range(0, int(end)):
                for j in range(0, int(end)):
                    self.addLink(
                        self.CoreSwitchList[i*end+j],
                        self.AggSwitchList[x+i],
                        bw=bw_c2a)

        for x in range(0, int(self.iAggLayerSwitch), end):
            for i in range(0, end):
                for j in range(0, end):
                    self.addLink(
                        self.AggSwitchList[x+i], self.EdgeSwitchList[x+j],
                        bw=bw_a2e)

        for x in range(0, int(self.iEdgeLayerSwitch)):
            for i in range(0, self.density):
                self.addLink(
                    self.EdgeSwitchList[x],
                    self.HostList[self.density * x + i],
                    bw=bw_h2e)

    def set_ovs_protocol(self,):
        self._set_ovs_protocol(self.CoreSwitchList)
        self._set_ovs_protocol(self.AggSwitchList)
        self._set_ovs_protocol(self.EdgeSwitchList)

    def _set_ovs_protocol(self, sw_list):
            for sw in sw_list:
                cmd = "sudo ovs-vsctl set bridge %s protocols=OpenFlow13" % sw
                os.system(cmd)

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


def iperfTest(net, topo):
    h1000, h1015, h1016 = net.get(
        topo.HostList[0], topo.HostList[14], topo.HostList[15])

    #iperf Server
    h1000.popen(
        'iperf -s -u -i 1 > iperf_server_differentPod_result', shell=True)

    #iperf Server
    h1015.popen(
        'iperf -s -u -i 1 > iperf_server_samePod_result', shell=True)

    #iperf Client
    h1016.cmdPrint('iperf -c ' + h1000.IP() + ' -u -t 10 -i 1 -b 100m')
    h1016.cmdPrint('iperf -c ' + h1015.IP() + ' -u -t 10 -i 1 -b 100m')


def pingTest(net):
    net.pingAll()

def startServerSSH(net):
    for host in net.hosts:
        host.cmd("/usr/sbin/sshd -o UseDNS=no -u0 &")
        info(host.name,"start sshd listener in ", host.IP(), '\n' )

def createTopo(pod, density, ip="127.0.0.1", port=6653, bw_c2a=10, bw_a2e=10, bw_h2e=10):
    topo = Fattree(pod, density)
    topo.createTopo()
    topo.createLink(bw_c2a=bw_c2a, bw_a2e=bw_a2e, bw_h2e=bw_h2e)

    CONTROLLER_IP = ip
    CONTROLLER_PORT = port
    net = Mininet(topo=topo, link=TCLink, controller=None, autoSetMacs=True)
    net.addController(
        'controller', controller=RemoteController,
        ip=CONTROLLER_IP, port=CONTROLLER_PORT)
    net.start()

    startServerSSH(net)
    #dumpNodeConnections(net.hosts)
    #pingTest(net)
    #iperfTest(net, topo)

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    if os.getuid() != 0:
        info("need root")
    elif os.getuid() == 0:
        try:
            createTopo(4, 2)
        except:
            print("Error on start mininet. cleanup!")

        finally:
            cleanup()
            print("kill sshd listeners   kill -9 $(pgrep -f listener)")
            os.system("kill -9 $(pgrep -f listener)")
            os.system("kill -9 $(pgrep -f xterm)")
            os.system("service ssh restart")
