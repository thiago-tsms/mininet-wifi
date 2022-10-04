import sys
from turtle import position
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mininet.node import Controller, RemoteController, OVSKernelSwitch, IVSSwitch, UserSwitch


def start_teste(args):

    # link=wmediumd
    # wmediumd_mode=interference
    # noise_th=-91
    # fading_cof=3
    # controller= Cotroller
    # switch = UserAP -> suporta meter tables (OpenFlow)
    net = Mininet_wifi()

    info("*** Criando dispositivos \n")
    h1 = net.addHost('h1', mac='00:00:00:00:00:01', ip='10.0.0.1/24')
    #h2 = net.addHost('h2', mac='00:00:00:00:00:02', ip='10.0.0.2/24')
    #h3 = net.addHost('h3', mac='00:00:00:00:00:03', ip='10.0.0.3/24')

    sw1 = net.addSwitch('sw1', ip='10.0.0.10/24')
    sw2 = net.addSwitch('sw2', ip='10.0.0.11/24')
    sw3 = net.addSwitch('sw3', ip='10.0.0.12/24')

    ap1 = net.addAccessPoint('ap1', ip='10.0.0.20/24', ssid='new-ssid', mode='g', channel='1',position='50,50,0')
    ap2 = net.addAccessPoint('ap2', ip='10.0.0.21/24', ssid='new-ssid', mode='g', channel='1',position='85,175,0')
    ap3 = net.addAccessPoint('ap3', ip='10.0.0.22/24', ssid='new-ssid', mode='g', channel='1',position='175,70,0')
    
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:10', ip='10.0.0.30/24')
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:20', ip='10.0.0.31/24')
    sta3 = net.addStation('sta3', mac='00:00:00:00:00:30', ip='10.0.0.32/24')
    sta4 = net.addStation('sta4', mac='00:00:00:00:00:40', ip='10.0.0.33/24')

    c1 = net.addController('c1')
    c2 = net.addController('c2')
    c3 = net.addController('c3')

    info("*** Configura o modelo de propagação \n")
    net.setPropagationModel(model="logDistance", exp=4.3)

    info("*** Configura os nós Wifi \n")
    net.configureWifiNodes()

    info("*** Associa e cria os links \n")

    #  c1      c2      c3
    #  |       |       |
    # sw1 --- sw2 --- sw3 --- h1
    #  |       |       |
    # ap1     ap2     ap3

    net.addLink(sw1, sw2)
    net.addLink(sw1, sw3)
    #net.addLink(sw2, sw3) Fecha um loop, e não funciona

    net.addLink(h1, sw3)
    #net.addLink(h2, sw2)
    #net.addLink(h3, sw3)

    net.addLink(ap1, sw1)
    net.addLink(ap2, sw2)
    net.addLink(ap3, sw3)

    #net.addLink(sta1, ap1)
    #net.addLink(sta2, ap2)
    #net.addLink(sta3, ap3)

    info("*** Plotting Graph\n")
    net.plotGraph(max_x=300, max_y=300)

    # seed -> semente
    net.setMobilityModel(time=0, model='RandomDirection',max_x=200, max_y=200, seed=20)

    info("*** Inicia Rede \n")
    net.build()
    c1.start()
    c2.start()
    c3.start()
    sw1.start([c1])
    sw2.start([c2])
    sw3.start([c3]) 

    info("*** Rodando CLI \n")
    CLI(net)

    info("*** Parando Rede \n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    start_teste(sys.argv)