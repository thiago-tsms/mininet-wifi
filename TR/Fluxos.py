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
mice_flow_max = 10240  # KBytes = 10MB
elephant_flow_min = 10240  # KBytes = 10MB
elephant_flow_max = 1024*1024*10  # KBytes = 10 GB

# FLOWS
# n_mice_flows = 45
# n_elephant_flows = 5
# n_iot_flows = 0

# L4 PROTOCOLS
protocol_list = ['--udp', '']  # udp / tcp
port_min = 1025
port_max = 65536

# IPERF SETTINGS
sampling_interval = '1'  # seconds


# ELEPHANT FLOW PARAMS
elephant_bandwidth_list = ['10M', '20M', '30M', '40M', '50M', '60M', '70M', '80M', '90M', '100M',
                           '200M', '300M', '400M', '500M', '600M', '700M', '800M', '900M', '1000M']

# MICE FLOW PARAMS
mice_bandwidth_list = ['100K', '200K', '300K', '400K', '500K', '600K', '700K', '800K', '900K', '1000K',
                       '2000K', '3000K', '4000K', '5000K', '6000K', '7000K', '8000K', '9000K', '10000K', '1000K']


def coleta_tcpdum(net):
    """
        Coleta os dados e salvo usando tcpdump (.pcao)
    """
    sw5 = net.get('sw5')
    sw5.cmdPrint('tcpdump -i sw5-eth1 -w sw5-eth1.pcap &')
    sw5.cmdPrint('tcpdump -i sw5-eth2 -w sw5-eth2.pcap &')
    sw5.cmdPrint('tcpdump -i sw5-eth3 -w sw5-eth3.pcap &')
    sw5.cmdPrint('tcpdump -i sw5-eth4 -w sw5-eth4.pcap &')

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
    #hosts = net.hosts
    #print(net)
    #print(f'hosts: {hosts}')

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
    dst.cmdPrint(server_cmd)
    src.cmdPrint(client_cmd)


def generate_mice_flows(id, duration, net, log_dir):

    """
    Generate mice flows
    May use either tcp or udp
    """

    hosts = net.stations
    #hosts = net.hosts
    #print(f'hosts: {hosts}')

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
    
    print("Setting random flow start times")

    # setting random flow start times
    flow_start_time = []
    for i in range(n_total_flows):
        n = random.randint(1, interval)
        if i == 0:
            flow_start_time.append(0)
        else:
            flow_start_time.append(flow_start_time[i - 1] + n)

    print("Setting random flow end times")
    # setting random flow end times
    # using normal distribution
    # we will keep duration till 95% of the total duration
    # the remaining 5% will be used as buffer to finish off the existing flows
    flow_end_time = []
    for i in range(n_total_flows):
        s = flow_start_time[i]
        #e = int(float(0.95) * float(duration))  # 95% of the duration
        end_time = random.randint(s, duration)
        #end_time = random_normal_number(s, e)
        print(f'endtime = {end_time}')
        #while end_time > e:
        #    print(f'end = {end_time} e e = {e}')
        #    end_time = random_normal_number(s, e)
        #while end_time > e:
        #    print(f'end = {end_time} e e = {e}')
        #    end_time = random_normal_number(s, e)
        flow_end_time.append(end_time)

    print("calculating flow duration")
	
    # calculating flow duration from start time and end time generated above
    flow_duration = []
    for i in range(n_total_flows):
        flow_duration.append(flow_end_time[i] - flow_start_time[i])

    print(flow_type)
    print(flow_start_time)
    print(flow_end_time)
    print(flow_duration)
    print("Remaining duration :" + str(duration - flow_start_time[-1]))

    # generating the flows
    for i in range(n_total_flows):
        if i == 0:
            time.sleep(flow_start_time[i])
        else:
            time.sleep(flow_start_time[i] - flow_start_time[i-1])
        if flow_type[i] == 'E':
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