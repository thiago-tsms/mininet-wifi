import sys
import re
import socket

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference
from json import dumps
from requests import put
from mininet.util import quietRun
from os import listdir, environ
from fcntl import ioctl
from array import array
from struct import pack, unpack

def getIfInfo(dst):
    is_64bits = sys.maxsize > 2**32
    struct_size = 40 if is_64bits else 32
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    max_possible = 8 # initial value
    while True:
      bytes = max_possible * struct_size
      names = array('B')
      for i in range(0, bytes):
        names.append(0)
      outbytes = unpack('iL', ioctl(
        s.fileno(),
        0x8912,  # SIOCGIFCONF
        pack('iL', bytes, names.buffer_info()[0])
      ))[0]
      if outbytes == bytes:
        max_possible *= 2
      else:
        break
    s.connect((dst, 0))
    ip = s.getsockname()[0]
    for i in range(0, outbytes, struct_size):
      addr = socket.inet_ntoa(names[i+20:i+24])
      if addr == ip:
        name = names[i:i+16]
        try:
          name = name.tobytes().decode('utf-8')
        except AttributeError:
          name = name.tostring()
        name = name.split('\0', 1)[0]
        return (name,addr)


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
    ap2 = net.addAccessPoint('ap2', failMode='standalone', ssid='ssid-ap2', mode='g', channel='1', position='150,50,0')
    ap3 = net.addAccessPoint('ap3', failMode='standalone', ssid='ssid-ap3', mode='g', channel='1', position='150,150,0')
    ap4 = net.addAccessPoint('ap4', failMode='standalone', ssid='ssid-ap4', mode='g', channel='1', position='50,150,0')

    info("*** Criando Stations \n")
    sta1 = net.addStation('sta1', ip='10.0.0.31/24', position='70,70,0', min_x=20, min_y=20, max_x=180, max_y=180, range=20)
    sta2 = net.addStation('sta2', ip='10.0.0.32/24', position='130,70,0', min_x=20, min_y=20, max_x=180, max_y=180, range=20)
    sta3 = net.addStation('sta3', ip='10.0.0.33/24', position='130,130,0', min_x=20, min_y=20, max_x=180, max_y=180, range=20)
    sta4 = net.addStation('sta4', ip='10.0.0.34/24', position='70,130,0', min_x=20, min_y=20, max_x=180, max_y=180, range=20)

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
    
    info("*** Configurando Mobilidade \n")
    net.setMobilityModel(time=0, model='RandomDirection', min_x=70, max_x=230, min_y=70, max_y=230, seed=20, ac_method='ssf')

    info("*** Plotando Gráfico \n")
    if '-p' in args:
        net.plotGraph(min_x=-10, min_y=-10, max_x=210, max_y=210)
        
    sta1.coord = ['70.0,70.0,0.0']
    sta2.coord = ['230.0,70.0,0.0']
    sta3.coord = ['230.0,180.0,0.0']
    sta4.coord = ['70.0,180.0,0.0']
    
    net.mobility(sta1, 'start', time=1)
    net.mobility(sta2, 'start', time=1)
    net.mobility(sta3, 'start', time=1)
    net.mobility(sta4, 'start', time=1)
     
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

    #monitoramento
    if '-m' in args:
        info("*** Configurando sFlow-RT \n")
        collector = environ.get('COLLECTOR','127.0.0.1')
        (ifname, agent) = getIfInfo(collector)
        sampling = environ.get('SAMPLING','10')
        polling = environ.get('POLLING','10')
        sflow = 'ovs-vsctl -- --id=@sflow create sflow agent=%s target=%s sampling=%s polling=%s --' % (ifname,collector,sampling,polling)

        info("*** Configurando sFlow-RT at Switches \n")
        for s in net.switches:
            sflow += ' -- set bridge %s sflow=@sflow' % s
            info(' '.join([s.name for s in net.switches]) + "\n")
            quietRun(sflow)

        info("*** Enviando topology \n")
        topo = {'nodes':{}, 'links':{}}
        '''for ap in net.aps:
            topo['nodes'][ap.name] = {'agent':agent, 'ports':{}}'''

        for s in net.switches:
            topo['nodes'][s.name] = {'agent':agent, 'ports':{}}
        path = '/sys/devices/virtual/mac80211_hwsim/'
        for child in listdir(path):
            dir_ = '/sys/devices/virtual/mac80211_hwsim/'+'%s' % child+'/net/'
            for child_ in listdir(dir_):
                node = child_[:3]
                if node in topo['nodes']:
                    ifindex = open(dir_+child_+'/ifindex').read().split('\n',1)[0]
                    topo['nodes'][node]['ports'][child_] = {'ifindex': ifindex}

        path = '/sys/devices/virtual/net/'
        for child in listdir(path):
            parts = re.match('(^.+)-(.+)', child)
            if parts is None: continue
            if parts.group(1) in topo['nodes']:
                ifindex = open(path+child+'/ifindex').read().split('\n',1)[0]
                topo['nodes'][parts.group(1)]['ports'][child] = {'ifindex': ifindex}

        linkName = '%s-%s' % (sw1.name, sw5.name)
        topo['links'][linkName] = {'node1': sw1.name, 'port1': 'sw1-eth2', 'node2': sw5.name,   'port2': 'sw5-eth1'}
        linkName = '%s-%s' % (sw2.name, sw5.name)
        topo['links'][linkName] = {'node1': sw2.name, 'port1': 'sw2-eth2', 'node2': sw5.name,   'port2': 'sw5-eth2'}
        linkName = '%s-%s' % (sw3.name, sw5.name)
        topo['links'][linkName] = {'node1': sw3.name, 'port1': 'sw3-eth2', 'node2': sw5.name,   'port2': 'sw5-eth3'}
        linkName = '%s-%s' % (sw4.name, sw5.name)
        topo['links'][linkName] = {'node1': sw4.name, 'port1': 'sw4-eth2', 'node2': sw5.name,   'port2': 'sw5-eth4'}

        put('http://127.0.0.1:8008/topology/json', data=dumps(topo))

    info("*** Rodando CLI \n")
    CLI(net)

    info("*** Parando Rede \n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    start_teste(sys.argv)
