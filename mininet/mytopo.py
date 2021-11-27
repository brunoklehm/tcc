from mn_wifi.topo import Topo


class MyTopo(Topo):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add router
        router = self.addAccessPoint('ap1', ssid='new-ssid', mode='g', channel='1', failMode="standalone", mac='00:00:00:00:00:01')
        
        # Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Add hosts
        tablet = self.addHost('tablet', mac='00:00:00:00:00:02', ip='10.0.0.5/8')
        sensor = self.addStation('sensor', mac='00:00:00:00:00:03', ip='10.0.0.10/8')
        datacenter = self.addHost('datacenter', mac='00:00:00:00:00:04', ip='10.0.0.15/8')
        cloud = self.addHost('cloud', mac='00:00:00:00:00:05', ip='10.0.0.20/8')

        # Add links
        self.addLink( tablet, router )
        self.addLink( sensor, router )
        self.addLink( datacenter, s1 )
        self.addLink( s1, router, delay='20ms' )
        self.addLink( s1, s2 )
        self.addLink( cloud, s2, delay='50ms' )


topos = { 'mytopo': ( lambda: MyTopo() ) }
