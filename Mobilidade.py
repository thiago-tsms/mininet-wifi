import sys
from turtle import position
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi


def start_teste(args):
    net = Mininet_wifi()

    info("*** Criando dispositivos \n")
    h1 = net.addHost('h1', mac='00:00:00:00:00:01', ip='10.0.0.1/8')
    h2 = net.addHost('h2', mac='00:00:00:00:00:02', ip='10.0.0.2/8')
    h3 = net.addHost('h3', mac='00:00:00:00:00:03', ip='10.0.0.3/8')

    ap1 = net.addAccessPoint('ap1', ssid='new-ssid', mode='g', channel='1',position='40,30,0')
    ap2 = net.addAccessPoint('ap2', ssid='new-ssid', mode='g', channel='1',position='80,150,0')
    ap3 = net.addAccessPoint('ap3', ssid='new-ssid', mode='g', channel='1',position='150,40,0')
    
    sta1 = net.addStation('sta1', mac='00:00:00:00:00:10', ip='10.0.0.10/8')
    sta2 = net.addStation('sta2', mac='00:00:00:00:00:20', ip='10.0.0.11/8')
    sta3 = net.addStation('sta3', mac='00:00:00:00:00:30', ip='10.0.0.12/8')
    sta4 = net.addStation('sta4', mac='00:00:00:00:00:40', ip='10.0.0.13/8')

    c1 = net.addController('c1')

    info("*** Configura o modelo de propagação \n")
    net.setPropagationModel(model="logDistance", exp=4.5)

    info("*** Configura os nós Wifi \n")
    net.configureWifiNodes()

    info("*** Associa e cria os links \n")
    net.addLink(ap1, h1)
    net.addLink(ap2, h2)
    net.addLink(ap3, h3)

    info("*** Plotting Graph\n")
    net.plotGraph()

    '''p1, p2, p3, p4 = {
        {'position': '40.0,100.0,0.0'},
        {'position': '60.0,80.0,0.0'},
        {'position': '80.0,60.0,0.0'},
        {'position': '90.0,40.0,0.0'}
    }

    net.mobility(sta1, 'start', time=1, **p1)
    net.mobility(sta1, 'stop', time=15, **p3)
    
    net.stopMobility(time=23)
    '''

    net.setMobilityModel(time=0, model='RandomDirection',max_x=180, max_y=180, seed=20)

    info("*** Inicia Rede \n")
    net.build()
    c1.start()
    ap1.start([c1])

    info("*** Rodando CLI \n")
    CLI(net)

    info("*** Parando Rede \n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    start_teste(sys.argv)