from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from mn_wifi.link import wmediumd
from mininet.log import info

def start_topologia(args):
    """
    Cria a topologia, 5 switch, 4 accessPoint e 4 station.
    argas:
        -mobility: ativa mobilidade.
        -p: plota a posição das station no gráfico.
    """

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
    ap2 = net.addAccessPoint('ap2', failMode='standalone', ssid='ssid-ap2', mode='g', channel='1', position='150,50,0')
    ap3 = net.addAccessPoint('ap3', failMode='standalone', ssid='ssid-ap3', mode='g', channel='1', position='150,150,0')
    ap4 = net.addAccessPoint('ap4', failMode='standalone', ssid='ssid-ap4', mode='g', channel='1', position='50,150,0')

    info("*** Criando Stations \n")
    sta1 = net.addStation('sta1', ip='10.0.0.31/24', position='60,60,0', min_x=20, min_y=20, max_x=180, max_y=180, range=27, txpower=4)
    sta2 = net.addStation('sta2', ip='10.0.0.32/24', position='140,60,0', min_x=20, min_y=20, max_x=180, max_y=180, range=27, txpower=4)
    sta3 = net.addStation('sta3', ip='10.0.0.33/24', position='140,140,0', min_x=20, min_y=20, max_x=180, max_y=180, range=27, txpower=4)
    sta4 = net.addStation('sta4', ip='10.0.0.34/24', position='60,140,0', min_x=20, min_y=20, max_x=180, max_y=180, range=27, txpower=4)

    info("*** Configurando o Modelo de Propagação \n")
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
    

    if '-m' in args:
        mobilidade(net)

    if '-p' in args:
        plot_posicao(net)
    

    info("*** Inicia Rede \n")
    net.build()

    info("*** Iniciando Rede \n")
    ap1.start([])
    ap2.start([])
    ap3.start([])
    ap4.start([])

    sw1.start([])
    sw2.start([])
    sw3.start([])
    sw4.start([])
    sw5.start([])

    return net


def mobilidade(net):
    """
    Inicia Mobilidade.
    Ainda não implementada
    """
    info("*** Configurando Mobilidade \n")
    net.setMobilityModel(time=0, model='RandomDirection', min_x=70, max_x=230, min_y=70, max_y=230, seed=20, ac_method='ssf')


def plot_posicao(net):
    """
    Plota no gráfico a posição das station.
    """
    info("*** Plotando Gráfico \n")
    net.plotGraph(min_x=-10, min_y=-10, max_x=210, max_y=210)
        

def start_coleta_tcpdum(net):
    """
        Inicia coleta de dados e salva usando tcpdump (.pcap)
    """
    sw5 = net.get('sw5')
    sw5.cmdPrint('tcpdump -i sw5-eth1 -w sw5-eth1.pcap &')
    sw5.cmdPrint('tcpdump -i sw5-eth2 -w sw5-eth2.pcap &')
    sw5.cmdPrint('tcpdump -i sw5-eth3 -w sw5-eth3.pcap &')
    sw5.cmdPrint('tcpdump -i sw5-eth4 -w sw5-eth4.pcap &')
    sw5.cmdPrint('tcpdump -i any -w sw5-any.pcap &')


def stop_coleta_tcpdum(net):
    """
    Finaliza a coleta de dados.
    """
    net.get('sw5').cmdPrint('killall tcpdump')
