import sys
from turtle import position
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mininet.node import Host, Node
from mininet.link import TCLink, Intf
from mininet.node import Controller, RemoteController, OVSKernelSwitch, IVSSwitch, UserSwitch


def start_teste(args):

    # link=wmediumd
    # wmediumd_mode=interference
    # noise_th=-91
    # fading_cof=3
    # controller= Cotroller
    # switch = UserAP -> suporta meter tables (OpenFlow)
    net = Mininet_wifi(topo=None)
    
    info("*** Criando switches \n")
    sw1 = net.addSwitch('sw1', ip='10.0.0.11/24')
    sw2 = net.addSwitch('sw2', ip='10.0.0.12/24')
    sw3 = net.addSwitch('sw3', ip='10.0.0.13/24')
    sw4 = net.addSwitch('sw4', ip='10.0.0.14/24')
    sw5 = net.addSwitch('sw5', ip='10.0.0.15/24')
    
    net.addLink(sw1, sw5, intfName1='sw1-sw5', cls=TCLink)
    net.addLink(sw2, sw5, intfName1='sw2-sw5', cls=TCLink)
    net.addLink(sw3, sw5, intfName1='sw3-sw5', cls=TCLink)
    net.addLink(sw4, sw5, intfName1='sw4-sw5', cls=TCLink)
    
    net.addLink(sw1, sw2, intfName1='sw1-sw2', cls=TCLink)
    net.addLink(sw3, sw4, intfName1='sw3-sw4', cls=TCLink)
    
    # sw3----------sw4
    #         |
    #        sw5 
    #         |      
    # sw1----------sw2

    info("*** Criando Access Points \n")
#     ap1 = net.addAccessPoint('ap1', ip='10.0.0.20/24', ssid='new-ssid', mode='g', channel='1', position='50,50,0')
#     ap2 = net.addAccessPoint('ap2', ip='10.0.0.21/24', ssid='new-ssid', mode='g', channel='1', position='85,175,0')
#     ap3 = net.addAccessPoint('ap3', ip='10.0.0.22/24', ssid='new-ssid', mode='g', channel='1', position='175,70,0')
#     ap4 = net.addAccessPoint('ap3', ip='10.0.0.22/24', ssid='new-ssid', mode='g', channel='1', position='175,70,0')
    
    info("*** Criando Stations \n")
#     sta1 = net.addStation('sta1', mac='00:00:00:00:00:10', ip='10.0.0.30/24')
#     sta2 = net.addStation('sta2', mac='00:00:00:00:00:20', ip='10.0.0.31/24')
#     sta3 = net.addStation('sta3', mac='00:00:00:00:00:30', ip='10.0.0.32/24')
#     sta4 = net.addStation('sta4', mac='00:00:00:00:00:40', ip='10.0.0.33/24')
    
    
    
#     r1 = net.addHost('r1', cls=Node, ip='0.0.0.0')
    
#     info("*** Criando hosts \n")
#     h1 = net.addHost('h1', cls=Host, ip='10.0.1.10/24', defaultRoute='10.0.1.1')
#     h2 = net.addHost('h2', cls=Host, ip='10.0.2.10/24', defaultRoute='10.0.2.1')
#     h3 = net.addHost('h3', cls=Host, ip='10.0.3.10/24', defaultRoute='10.0.3.1')
#     h4 = net.addHost('h4', cls=Host, ip='10.0.4.10/24', defaultRoute='10.0.4.1')

    #h1.cmd("route add default gw 10.0.1.1")
    #h2.cmd("route add default gw 10.0.2.1")
    #h3.cmd("route add default gw 10.0.3.1")
    #h4.cmd("route add default gw 10.0.4.1")


    #sw1 = net.addSwitch('sw1', ip='10.0.0.10/24')
    #sw2 = net.addSwitch('sw2', ip='10.0.0.11/24')
    #sw3 = net.addSwitch('sw3', ip='10.0.0.12/24')

    #ap1 = net.addAccessPoint('ap1', ip='10.0.0.20/24', ssid='new-ssid', mode='g', channel='1',position='50,50,0')
    #ap2 = net.addAccessPoint('ap2', ip='10.0.0.21/24', ssid='new-ssid', mode='g', channel='1',position='85,175,0')
    #ap3 = net.addAccessPoint('ap3', ip='10.0.0.22/24', ssid='new-ssid', mode='g', channel='1',position='175,70,0')
    
    #sta1 = net.addStation('sta1', mac='00:00:00:00:00:10', ip='10.0.0.30/24')
    #sta2 = net.addStation('sta2', mac='00:00:00:00:00:20', ip='10.0.0.31/24')
    #sta3 = net.addStation('sta3', mac='00:00:00:00:00:30', ip='10.0.0.32/24')
    #sta4 = net.addStation('sta4', mac='00:00:00:00:00:40', ip='10.0.0.33/24')

    #c1 = net.addController('c1')
    #c2 = net.addController('c2')
    #c3 = net.addController('c3')

    info("*** Configura o modelo de propagação \n")
    #net.setPropagationModel(model="logDistance", exp=4.3)

    info("*** Configura os nós Wifi \n")
    #net.configureWifiNodes()

    info("*** Associa e cria os links \n")

    #         h2
    #         |
    # h1 --- r1 --- r3
    #         |      
    #         h4     

    net.addLink(r1, h1, intfName1='r1-eth1', cls=TCLink)
    net.addLink(r1, h2, intfName1='r1-eth2', cls=TCLink)
    net.addLink(r1, h3, intfName1='r1-eth3', cls=TCLink)
    net.addLink(r1, h4, intfName1='r1-eth4', cls=TCLink)

    info( '*** Estabelecendo Rotas \n')
    #r1.cmd("route add default gw 10.0.2.2")
    #r1.cmd("route add -net 10.0.11.0/24 gw 10.0.1.2")
    #r1.cmd("route add -net 10.0.13.0/24 gw 10.0.3.2")
    #r1.cmd("route add -net 10.0.13.0/24 gw 10.0.3.2")

    #net.addLink(h1, sw3)
    #net.addLink(h2, sw2)
    #net.addLink(h3, sw3)

    #net.addLink(ap1, sw1)
    #net.addLink(ap2, sw2)
    #net.addLink(ap3, sw3)

    #net.addLink(sta1, ap1)
    #net.addLink(sta2, ap2)
    #net.addLink(sta3, ap3)

    info("*** Plotting Graph\n")
    #net.plotGraph(max_x=300, max_y=300)

    # seed -> semente
    #net.setMobilityModel(time=0, model='RandomDirection',max_x=200, max_y=200, seed=20)

    info("*** Inicia Rede \n")
    net.build()

    info( '*** Iniciando Controladores \n')
    for controller in net.controllers:
        controller.start()

    info( '*** Configurando Roteador \n')
    #sysctl - configura parâmetro de kernel em tempo de execução, a configuração é volátil
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')

    info( '*** Atribuindo IP para as interfaces de rede \n')
    #ifconfig - configura interface de rede
    r1.cmd("ifconfig r1-eth1 10.0.1.1/24")
    r1.cmd("ifconfig r1-eth2 10.0.2.1/24")
    r1.cmd("ifconfig r1-eth3 10.0.3.1/24")
    r1.cmd("ifconfig r1-eth4 10.0.4.1/24")

    info( '*** Estabelecendo Rotas \n')
    #route - exibe ou modifica a tabela de roteamento IP
    h1.cmd("route add default gw 10.0.1.1")
    h2.cmd("route add default gw 10.0.2.1")
    h3.cmd("route add default gw 10.0.3.1")
    h4.cmd("route add default gw 10.0.4.1")

    info("*** Rodando CLI \n")
    CLI(net)

    info("*** Parando Rede \n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    start_teste(sys.argv)
