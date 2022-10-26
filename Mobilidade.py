import sys

from turtle import position
from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference

def start_teste(args):

    info("*** Cria rede \n")
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)
    
    info("*** Criando switches \n")
    sw1 = net.addSwitch('sw1', failMode='standalone')
    sw2 = net.addSwitch('sw2', failMode='standalone')
    sw3 = net.addSwitch('sw3', failMode='standalone')
    sw4 = net.addSwitch('sw4', failMode='standalone')
    sw5 = net.addSwitch('sw5', failMode='standalone')

    info("*** Criando Access Points \n")
    ap1 = net.addAccessPoint('ap1', failMode='standalone', ssid='ssid-ap1', mode='g', channel='1', position='50,50,0')
    ap2 = net.addAccessPoint('ap2', failMode='standalone', ssid='ssid-ap2', mode='g', channel='1', position='250,50,0')
    ap3 = net.addAccessPoint('ap3', failMode='standalone', ssid='ssid-ap3', mode='g', channel='1', position='250,200,0')
    ap4 = net.addAccessPoint('ap4', failMode='standalone', ssid='ssid-ap4', mode='g', channel='1', position='50,200,0')

    info("*** Criando Stations \n")
    sta1 = net.addStation('sta1', ip='10.0.0.31/24', position='55,55,0')
    sta2 = net.addStation('sta2', ip='10.0.0.32/24', position='245,55,0')
    sta3 = net.addStation('sta3', ip='10.0.0.33/24', position='245,195,0')
    sta4 = net.addStation('sta4', ip='10.0.0.34/24', position='55,205,0')

    info("*** Configura o modelo de propagação \n")
    net.setPropagationModel(model="logDistance", exp=4.3)

    info("*** Configura os nós Wifi \n")
    net.configureWifiNodes()

    info("*** Faz os links \n")
    net.addLink(ap1, sw1)
    net.addLink(ap2, sw2)
    net.addLink(ap3, sw3)
    net.addLink(ap4, sw4)

    net.addLink(sw1, sw5)
    net.addLink(sw2, sw5)
    net.addLink(sw3, sw5)
    net.addLink(sw4, sw5)

    info("*** Plotting Graph\n")
    net.plotGraph(max_x=300, max_y=300)
     
    info("*** Inicia Rede \n")
    net.build()

    info("*** Faz conexões \n")
    ap1.start([])
    ap2.start([])
    ap3.start([])
    ap4.start([])

    sw1.start([])
    sw2.start([])
    sw3.start([])
    sw4.start([])
    sw5.start([])

    info("*** Rodando CLI \n")
    CLI(net)

    info("*** Parando Rede \n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    start_teste(sys.argv)
    
