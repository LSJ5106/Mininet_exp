#!/usr/bin/python
# 包含2个交换机的核心层、4个交换机的汇聚层和4个交换机的接入层
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController

class FatTree(Topo):
    def __init__(self):
        Topo.__init__(self)

        # Core switches
        # 2个交换机的核心层
        core1 = self.addSwitch('c1')
        core2 = self.addSwitch('c2')

        # Aggregation switches
        # 4个交换机的汇聚层
        for i in range(4):
            agg = self.addSwitch('a%s' % (i + 1))

            # Connect aggregation switches to core switches
            self.addLink(agg, core1)
            self.addLink(agg, core2)

            # Access switches
            # 4个交换机的接入层
            for j in range(4):
                access = self.addSwitch('s%s%s' % (i + 1, j + 1))

                # Connect access switches to aggregation switches
                self.addLink(access, agg)

                # Hosts
                for k in range(2):
                    host = self.addHost('h%s%s%s' % (i + 1, j + 1, k + 1))

                    # Connect hosts to access switches
                    self.addLink(host, access)

topos = {'fattree': FatTree}

if __name__ == '__main__':
    topo = FatTree()
    net = Mininet(topo=topo, controller=lambda name: RemoteController(name, ip='127.0.0.1'), autoSetMacs=True)
    net.start()
    net.pingAll()
    net.stop()