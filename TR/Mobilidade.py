from Fluxos import *
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

from os import path
from os import mkdir
import random
import time
import numpy as np


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

    info("*** Configurando o Modelo de Propaga????o \n")
    net.setPropagationModel(model="logDistance", exp=4.3)

    info("*** Configura os n??s Wifi \n")
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
    
    #print(f'net: {net.stations}')
    #print(f'net: {dir(net)}')
    
    if '-mobility' in args:
        info("*** Configurando Mobilidade \n")
        net.setMobilityModel(time=0, model='RandomDirection', min_x=70, max_x=230, min_y=70, max_y=230, seed=20, ac_method='ssf')

    info("*** Plotando Gr??fico \n")
    if '-p' in args:
        net.plotGraph(min_x=-10, min_y=-10, max_x=210, max_y=210)
        
    if '-mobility' in args:
        sta1.coord = ['70.0,70.0,0.0']
        sta2.coord = ['230.0,70.0,0.0']
        sta3.coord = ['230.0,180.0,0.0']
        sta4.coord = ['70.0,180.0,0.0']

        net.mobility(sta1, 'start', time=1)
        net.mobility(sta2, 'start', time=1)
        net.mobility(sta3, 'start', time=1)
        net.mobility(sta4, 'start', time=1)
     
    info("**(num)in args:
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
    
    log_dir = "./test"
    
    # creating log directory
    # log_dir = path.expanduser('~') + log_dir
    # i = 1
    # while True:
    #    if not path.exists(log_dir + str(i)):
    #        # mkdir(log_dir + str(i))
    #        log_dir = log_dir + str(i)
    #        break
    #    i = i+1
    
    experiment_duration = int(input("Experiment duration: "))
    n_elephant_flows = int(input("No of elephant flows: "))
    n_mice_flows = int(input("No of mice flows: "))

    coleta_tcpdum(net)
    generate_flows(n_elephant_flows, n_mice_flows, experiment_duration, net, log_dir)

    info("*** Rodando CLI \n")
    CLI(net)

    #generate_flows(n_elephant_flows, n_mice_flows, experiment_duration, net, log_dir)

    info("*** Parando Rede \n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    start_teste(sys.argv)
