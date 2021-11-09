"""Custom topology example

Two directly connected switches plus a host for each switch:

   host --- switch --- switch --- host

Adding the 'topos' dict with a key/value pair to generate our newly defined
topology enables one to pass in '--topo=mytopo' from the command line.
"""

from mn_wifi.topo import Topo


class MyTopo(Topo):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        ap1 = self.addAccessPoint('ap1', ssid='new-ssid', mode='g', channel='1', failMode="standalone", mac='00:00:00:00:00:01', position='50,50,0')
        sta1 = self.addStation('sta1', mac='00:00:00:00:00:02', ip='10.0.0.1/8', position='236.0,313.0,0')
        sta2 = self.addStation('sta2', mac='00:00:00:00:00:03', ip='10.0.0.2/8', position='395.0,333.0,0')
        sta3 = self.addStation('sta3', mac='00:00:00:00:00:04', ip='10.0.0.3/8', position='555.0,304.0,0')
        sta4 = self.addStation('sta4', mac='00:00:00:00:00:05', ip='10.0.0.4/8', position='600.0,175.0,0')
        h1 = self.addHost('h1', ip='10.0.0.5/8')

        # Add links
        self.addLink( sta1, ap1 )
        self.addLink( sta2, ap1 )
        self.addLink( sta3, ap1 )
        self.addLink( sta4, ap1 )
        self.addLink( h1, ap1 )


topos = { 'mytopo': ( lambda: MyTopo() ) }
