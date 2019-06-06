#!/usr/bin/env python

import time
import timeit
import socket
import select
import multiprocessing
from datetime import datetime

class tcp_tester():
    def __init__(self, dst, port):
        self.dst = dst
        self.port = port
        self.setup()
    def __del__(self):
        self.sock.close()
    def setup(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def connect(self):
        try:
            self.sock.connect((self.dst,self.port))
        except socket.error as E:
            if E.errno == 111:
                pass
            else:
                print E
        except Exception as E:
                print E

class ping_tester():
    packet = '\x08\x00\x9c\xa2\x00\x00\x00\x00[]' # pre-calculated basic icmp echo request with zeroed id and seq number and empty data complete with matching checksum
    ICMP_MAX_RECV = 2048 # Max size of incoming buffer
    def __init__(self, dst, timeout=1):
        self.dst = dst
        self.timeout = timeout / 1000.0 # convert s to ms
        self.setup()
    def __del__(self):
        self.sock.close()
    def setup(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    def connect(self):
        # send packet
        self.sock.sendto(self.packet, (self.dst, 1)) # Port number is irrelevant for ICMP
        # wait until we timeout or receive data back
        inputready, outputready, exceptready = select.select([self.sock], [], [], self.timeout)
        if inputready == []: # timeout
            return 1000 # return value of 1000 on timeout not that we are caring about the value
        # Receive the actual data Not sure if this is needed might be able to move this into __del__
        packet_data, address = self.sock.recvfrom(self.ICMP_MAX_RECV)

def time_tcp_connection(dst, port):
    import time
    start_time = time.time()
    results = []
    timer = timeit.Timer('tester.connect()', setup='from __main__ import tcp_tester; tester = tcp_tester("%s", %s)' %(dst, port))
    while time.time() - start_time <= 1.0000:
        results.append(timer.timeit(1))
        time.sleep(0.4)
    base_metric = 'test.tcp.%s.' %(dst.replace('.','_'))
    print('len_results for %s: %s' %(base_metric, len(results)))
    time = int(start_time)
    graphite_message = ''
    graphite_message += '%s %s %d \n' %(base_metric + "min", min(results) * 1000, time)
    graphite_message += '%s %s %d \n' %(base_metric + "max", max(results) * 1000, time)
    graphite_message += '%s %s %d \n' %(base_metric + "average", (float(sum(results))/float(len(results))) * 1000, time)
    send_graphite_message(graphite_message)

def time_ping_connection(dst, timeout):
    import time
    start_time = time.time()
    results = []
    timer = timeit.Timer('tester.connect()', setup='from __main__ import ping_tester; tester = ping_tester("%s", %s)' %(dst, timeout))
    while time.time() - start_time <= 1.0000:
        results.append(timer.timeit(1))
        time.sleep(0.4)
    base_metric = 'test.ping.%s.' %(dst.replace('.','_'))
    print('len_results for %s: %s' %(base_metric, len(results)))
    time = int(start_time)
    graphite_message = ''
    graphite_message += '%s %s %d \n' %(base_metric + "min", min(results) * 1000, time)
    graphite_message += '%s %s %d \n' %(base_metric + "max", max(results) * 1000, time)
    graphite_message += '%s %s %d \n' %(base_metric + "average", (float(sum(results))/float(len(results))) * 1000, time)
    send_graphite_message(graphite_message)

#def send_to_graphite(metric, value, time=None, host="127.0.0.1", port=2003):
#    if not time:
#        time = int(time.time())
#    sock = socket.socket()
#    sock.connect((host, port))
#    sock.send("%s %s %d \n" %(metric, value, time))
#    sock.close()
def send_graphite_message(message, host="127.0.0.1", port=2003):
    sock = socket.socket()
    sock.connect((host, port))
    sock.send(message)
    sock.close()

def time_forever(args=("192.168.0.1", 80)):
    while True:
        # setup new proc ready to run
        p = multiprocessing.Process(target=time_tcp_connection, args=args)
        # find and wait for next second boundry to start proc
        time.sleep((int(time.time()) + 1) - time.time())
        p.start()
        #print('starting tcp for %s' %(str(args)))

def time_forever_ping(args=("192.168.0.1", 1)):
    while True:
        # setup new proc ready to run
        p = multiprocessing.Process(target=time_ping_connection, args=args)
        # find and wait for next second boundry to start proc
        time.sleep((int(time.time()) + 1) - time.time())
        p.start()
        #print('starting ping for %s' %(str(args)))


if __name__ == '__main__':
    #ping_router_process = multiprocessing.Process(target=time_forever_ping)
    #tcp_router_process = multiprocessing.Process(target=time_forever)
    #ping_2nd_hop_process = multiprocessing.Process(target=time_forever_ping, kwargs={"args":("100.127.66.2", 5)})
    #tcp_2nd_hop_process = multiprocessing.Process(target=time_forever, kwargs={"args":("100.127.66.2", 80)})
    google_host = socket.gethostbyname('google.com')
    #ping_google_process = multiprocessing.Process(target=time_forever_ping, kwargs={"args":(google_host, 2)})
    tcp_google_process = multiprocessing.Process(target=time_forever, kwargs={"args":(google_host, 80)})
    #ping_router_process.start()
    #tcp_router_process.start()
    #ping_2nd_hop_process.start()
    #tcp_2nd_hop_process.start()
    #ping_google_process.start()
    tcp_google_process.start()
    while True:
        time.sleep(60)
