from topologia import *
from fluxos import *

import sys
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI

# FLOW SIZES
# 
# flows with 15 packets or greater is an elephant flow as per CISCO
# considering 1512 byte packets, elephant flow size is
# threshold = (14 * 1512)/1000 = 21.168 KBytes

def start_teste(args):

    net = start_topologia(args)
      
    if '-f' in args:
      experiment_duration = int(input("Experiment duration: "))
      n_elephant_flows = int(input("No of elephant flows: "))
      n_mice_flows = int(input("No of mice flows: "))
      
      # Inicia o log tcp dump
      start_coleta_tcpdum(net)
    
      # Gera e executa os flows
      generate_flows(n_elephant_flows, n_mice_flows, experiment_duration, net)
    
      # Encerra o log tcpdump
      stop_coleta_tcpdum(net)

    info("*** Rodando CLI \n")
    CLI(net)

    info("*** Parando Rede \n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    start_teste(sys.argv)