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


# GLOBAL VARIABLES
# experiment_duration = 180  # seconds
# controller_ip = '10.14.87.5'  # ubuntu_lab


# FLOW SIZES
# Calculations
#
# flows with 15 packets or greater is an elephant flow as per CISCO
# considering 1512 byte packets, elephant flow size is
#
# threshold = (14 * 1512)/1000 = 21.168 KBytes
#

mice_flow_min = 100  # KBytes = 100KB
mice_flow_max = 10000  # KBytes = 10MB
elephant_flow_min = 1000000  # KBytes = 1 GB
elephant_flow_max = 10000000  # KBytes = 10 GB

# FLOWS
# n_mice_flows = 45
# n_elephant_flows = 5
# n_iot_flows = 0

# L4 PROTOCOLS
# protocol_list = ['--udp', '']  # udp / tcp
protocol_list = ['']  # udp / tcp
port_min = 1025
port_max = 65536

# IPERF SETTINGS
sampling_interval = '1'  # seconds

# ELEPHANT FLOW PARAMS
elephant_bandwidth_list = ['1G', '2G', '3G', '4G', '5G', '6G', '7G', '8G', '9G', '10G']

# MICE FLOW PARAMS
mice_bandwidth_list = ['100K', '200K', '300K', '400K', '500K', '600K', '700K', '800K', '900K', '1000K',
                       '2000K', '3000K', '4000K', '5000K', '6000K', '7000K', '8000K', '9000K', '10000K']

def coleta_tcpdum(net):
    """
        Coleta os dados e salva usando tcpdump (.pcap)
    """
    sw5 = net.get('sw5')
    sw5.cmdPrint('tcpdump -i sw5-eth1 -w sw5-eth1.pcap &')
    sw5.cmdPrint('tcpdump -i sw5-eth2 -w sw5-eth2.pcap &')
    sw5.cmdPrint('tcpdump -i sw5-eth3 -w sw5-eth3.pcap &')
    sw5.cmdPrint('tcpdump -i sw5-eth4 -w sw5-eth4.pcap &')
    sw5.cmdPrint('tcpdump -i any -w sw5-any.pcap &')


def random_normal_number(low, high):
    range = high - low
    mean = int(float(range) * float(75) / float(100)) + low
    sd = int(float(range) / float(4))
    num = np.random.normal(mean, sd)
    return int(num)


def generate_elephant_flows(id, duration, net, log_dir):

    """
    Generate Elephant flows
    May use either tcp or udp
    """

    hosts = net.stations

    # select random src and dst
    end_points = random.sample(hosts, 2)
    src = net.get(str(end_points[0]))
    dst = net.get(str(end_points[1]))

    # select connection params
    protocol = random.choice(protocol_list)
    port_argument = str(random.randint(port_min, port_max))
    bandwidth_argument = random.choice(elephant_bandwidth_list)

    # create cmd
    server_cmd = "iperf -s "
    server_cmd += protocol
    server_cmd += " -p "
    server_cmd += port_argument
    server_cmd += " -i "
    server_cmd += sampling_interval
    server_cmd += " > "
    server_cmd += log_dir + "/elephant_flow_%003d" % id + ".txt 2>&1 "
    server_cmd += " & "

    client_cmd = "iperf -c "
    client_cmd += dst.IP() + " "
    client_cmd += protocol
    client_cmd += " -p "
    client_cmd += port_argument
    if protocol == "--udp":
        client_cmd += " -b "
        client_cmd += bandwidth_argument
    client_cmd += " -t "
    client_cmd += str(duration)
    client_cmd += " & "

    # send the cmd
    print(f"COMANDO ENVIADO:\n{server_cmd}\n")
    dst.cmdPrint(server_cmd)
    src.cmdPrint(client_cmd)
    

def generate_mice_hping(t, net):
    hosts = net.stations
    end_points = random.sample(hosts, 2)
    src = net.get(str(end_points[0]))
    dst = net.get(str(end_points[1]))
    d = random.randint(100, 10000)
    p = random.randint(1025, 65536)
    client_cmd = f"hping3 {dst.IP()} -d {d} -c {t} -q -p {p} --dontfrag &"
    src.cmdPrint(client_cmd)

    
def generate_flood_hping(t, net):
    hosts = net.stations
    end_points = random.sample(hosts, 2)
    src = net.get(str(end_points[0]))
    dst = net.get(str(end_points[1]))
    d = random.randint(10000, 65000)
    p = random.randint(1025, 65536)
    client_cmd = f"hping3 {dst.IP()} -d {d} -c {t*8} --fast -q -p {p} --dontfrag &"
    src.cmdPrint(client_cmd)
    
    
def generate_mice_flows(id, duration, net, log_dir):

    """
    Generate mice flows
    May use either tcp or udp
    """

    hosts = net.stations

    # select random src and dst
    end_points = random.sample(hosts, 2)
    src = net.get(str(end_points[0]))
    
    print(str(end_points[0]))
    print(src)
    dst = net.get(str(end_points[1]))

    # select connection params
    protocol = random.choice(protocol_list)
    port_argument = str(random.randint(port_min, port_max))
    bandwidth_argument = random.choice(mice_bandwidth_list)

    # create cmd
    server_cmd = "iperf -s "
    server_cmd += protocol
    server_cmd += " -p "
    server_cmd += port_argument
    server_cmd += " -i "
    server_cmd += sampling_interval
    server_cmd += " > "
    server_cmd += log_dir + "/mice_flow_%003d" % id + ".txt 2>&1 "
    server_cmd += " & "

    client_cmd = "iperf -c "
    client_cmd += dst.IP() + " "
    client_cmd += protocol
    client_cmd += " -p "
    client_cmd += port_argument
    if protocol == "--udp":
        client_cmd += " -b "
        client_cmd += bandwidth_argument
    client_cmd += " -t "
    client_cmd += str(duration)
    client_cmd += " & "

    # send the cmd
    dst.cmdPrint(server_cmd)
    src.cmdPrint(client_cmd)

def generate_pings(n_elephant_flows, n_mice_flows, duration, net):
    #generate_mice_hping(id, net)
  
    n_total_flows = n_elephant_flows + n_mice_flows
    interval = duration // n_total_flows

    # setting random mice flow or elephant flows
    flow_type = []
    for i in range(n_elephant_flows):
        flow_type.append('E')
    for i in range(n_mice_flows):
        flow_type.append('M')
    random.shuffle(flow_type)

    print("Setting uniform flow start times")
    flow_start_time = []
    for i in range(n_total_flows):
        flow_start_time.append(i * interval)

    print("Setting uniform flow end times")
    flow_end_time = []
    for i in range(n_total_flows):
        flow_end_time.append((i + 1) * interval)

    print("calculating flow duration")
    flow_duration = []
    for i in range(n_total_flows):
        flow_duration.append(flow_end_time[i] - flow_start_time[i])

    print(flow_type)
    print(flow_start_time)
    print(flow_end_time)
    print(flow_duration)
    print("Remaining duration :" + str(duration - flow_end_time[-1]))

    # generating the flows
    tempos = []
    tempo_inicial = time.time()
    for i in range(n_total_flows):
        if i == 0:
            time.sleep(flow_start_time[i])
        else:
            time.sleep(flow_start_time[i] - flow_start_time[i-1])
        if flow_type[i] == 'E':
            tempos.append(time.time()-tempo_inicial)
            for _ in range(random.randint(2, 8)):
                generate_mice_hping(flow_duration[i], net)
            generate_flood_hping(flow_duration[i], net)
        elif flow_type[i] == 'M':
            for _ in range(random.randint(2, 8)):
                generate_mice_hping(flow_duration[i], net)
            
    print("ELEPHANT FLOWS START TIME:")
    print(tempos)

    # sleeping for the remaining duration of the experiment
    remaining_duration = duration - flow_start_time[-1]
    info("Traffic started, going to sleep for %s seconds...\n " % remaining_duration)
    time.sleep(remaining_duration)

    # ending all the flows generated by
    info("Stopping traffic...\n")
  
def generate_flows(n_elephant_flows, n_mice_flows, duration, net, log_dir):
    """
    Generate elephant and mice flows randomly for the given duration
    """

    print("Generating flows")
    if not path.exists(log_dir):
        mkdir(log_dir)

    n_total_flows = n_elephant_flows + n_mice_flows
    interval = duration // n_total_flows

    # setting random mice flow or elephant flows
    flow_type = []
    for i in range(n_elephant_flows):
        flow_type.append('E')
    for i in range(n_mice_flows):
        flow_type.append('M')
    random.shuffle(flow_type)

    print("Setting uniform flow start times")
    flow_start_time = []
    for i in range(n_total_flows):
        flow_start_time.append(i * interval)

    print("Setting uniform flow end times")
    flow_end_time = []
    for i in range(n_total_flows):
        flow_end_time.append((i + 1) * interval)

    print("calculating flow duration")
    flow_duration = []
    for i in range(n_total_flows):
        flow_duration.append(flow_end_time[i] - flow_start_time[i])

    print(flow_type)
    print(flow_start_time)
    print(flow_end_time)
    print(flow_duration)
    print("Remaining duration :" + str(duration - flow_end_time[-1]))

    # generating the flows
    for i in range(n_total_flows):
        if i == 0:
            time.sleep(flow_start_time[i])
        else:
            time.sleep(flow_start_time[i] - flow_start_time[i-1])
        if flow_type[i] == 'E':
            print(f"ELEPHANT FLOW STARTED ON {flow_start_time[i]} BY {flow_duration[i]} SECONDS.")
            generate_elephant_flows(i, flow_duration[i], net, log_dir)
        elif flow_type[i] == 'M':
            generate_mice_flows(i, flow_duration[i], net, log_dir)

    # sleeping for the remaining duration of the experiment
    remaining_duration = duration - flow_start_time[-1]
    info("Traffic started, going to sleep for %s seconds...\n " % remaining_duration)
    time.sleep(remaining_duration)

    # ending all the flows generated by
    # killing the iperf sessions
    info("Stopping traffic...\n")
    info("Killing active iperf sessions...\n")

    # killing iperf in all the hosts
    for host in net.hosts:
        host.cmdPrint('killall -9 iperf')
        
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
    
    #print(f'net: {net.stations}')
    #print(f'net: {dir(net)}')
    
    if '-mobility' in args:
        info("*** Configurando Mobilidade \n")
        net.setMobilityModel(time=0, model='RandomDirection', min_x=70, max_x=230, min_y=70, max_y=230, seed=20, ac_method='ssf')

    info("*** Plotando Gráfico \n")
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
      
    if '-f' in args:
      log_dir = "./test"    
      experiment_duration = int(input("Experiment duration: "))
      n_elephant_flows = int(input("No of elephant flows: "))
      n_mice_flows = int(input("No of mice flows: "))
      
      # Inicia o log tcp dump
      coleta_tcpdum(net)
    
      # Gera e executa os flows
      generate_pings(n_elephant_flows, n_mice_flows, experiment_duration, net)
    
      # Encerra o log tcpdump
      net.get('sw5').cmdPrint('killall tcpdump')

    info("*** Rodando CLI \n")
    CLI(net)

    info("*** Parando Rede \n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    start_teste(sys.argv)
