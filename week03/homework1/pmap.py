import socket
import argparse
import os
import re
import ipaddress
import time
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from abc import ABCMeta


def check_ip(ipaddresses):
    ip_regEX = re.compile(r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(\-\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})?$")
    match = ip_regEX.match(ipaddresses)
    if match and match.group(0) == ipaddresses:
        return ipaddresses
    raise argparse.ArgumentTypeError(f'{ipaddresses} is an invalid ipaddress/ipaddress range')


parser = argparse.ArgumentParser(description='scan the network connection of the target ipaddress')
parser.add_argument('-n', '--number', type=int, metavar='', required=True,
                    help='number of concurrent running threads/processes')
parser.add_argument('-f', '--function', type=str, metavar='', required=True, choices=['ping', 'tcp'],
                    help='put argument as ping or tcp')
parser.add_argument('-ip', '--ipaddress', type=check_ip, metavar='', required=True,
                    help='accept ipaddress or ipaddress range, TCP should be single ipaddress')
parser.add_argument('-w', '--writeto', type=str, metavar='', help='output to the specified file')
parser.add_argument('-m', '--mode', type=str, metavar='', choices=['proc', 'thread'], default='thread',
                    help='proc|thread multi process or multi threading')
parser.add_argument('-v', '--verbose', action='store_true', help='print the time consumed by the scanner')

args = parser.parse_args()


class FunctionEnum(Enum):
    PING = 'ping'
    TCP = 'tcp'


class ModeEnum(Enum):
    PROC = 'proc'
    THREAD = 'thread'


class IPScannerBase(metaclass=ABCMeta):
    def __init__(self, ip_args, mode, worker_number):
        self.ip_args = ip_args.strip()
        self.mode = mode
        self.worker_number = worker_number if worker_number < os.cpu_count() else os.cpu_count()
        self.output_list = []

    def do_work(self):
        raise NotImplementedError

    def output_results(self):
        if self.output_list:
            if args.writeto:
                with open(args.writeto, 'w') as handler:
                    for item in self.output_list:
                        handler.write(item + '\n')
            else:
                for ele in self.output_list:
                    print(ele)
        else:
            print('No output')

    @staticmethod
    def get_ip_list(start_ip, end_ip):
        start_IP = ipaddress.IPv4Address(start_ip)
        end_IP = ipaddress.IPv4Address(end_ip)
        return list(map(lambda ip: str(ipaddress.IPv4Address(ip)), range(int(start_IP), int(end_IP) + 1)))


class IPScannerPing(IPScannerBase):
    def __init__(self, ip_args, mode, worker_number):
        super().__init__(ip_args, mode, worker_number)

    def ping_IP(self, ipaddress):
        try:
            return socket.gethostbyaddr(ipaddress)[2]
        except socket.gaierror:
            print('network error')
            pass
        except Exception:
            pass

    def do_work(self):
        if '-' not in self.ip_args:
            self.output_list = self.ping_IP(self.ip_args)
        else:
            full_ip_list = IPScannerBase.get_ip_list(self.ip_args.split('-')[0], self.ip_args.split('-')[1])

            try:
                if self.mode == ModeEnum.THREAD:
                    with ThreadPoolExecutor(self.worker_number) as thread_executor:
                        ipaddresses = thread_executor.map(self.ping_IP, full_ip_list)
                    self.output_list = list(ipaddresses)
                else:
                    with ProcessPoolExecutor(self.worker_number) as proc_executor:
                        ipaddresses = proc_executor.map(self.ping_IP, full_ip_list)
                    self.output_list = list(ipaddresses)
            except TimeoutError:
                print('Timeout')
        self.output_results()


class IPScannerTCP(IPScannerBase):
    def __init__(self, ip_args, mode, worker_number):
        super().__init__(ip_args, mode, worker_number)

    def scan_port(self, ip_port):
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip = ip_port[0]
        port = ip_port[1]
        location = (ip, port)
        result_of_check = a_socket.connect_ex(location)

        if result_of_check == 0:
            return ip_port
        else:
            return

    def do_work(self):
        if '-' not in self.ip_args:
            ips_ports = [(self.ip_args, port) for port in range(70, 81)]
        else:
            full_ip_list = IPScannerBase.get_ip_list(self.ip_args.split('-')[0], self.ip_args.split('-')[1])
            ips_ports = [(ip, port) for ip in full_ip_list for port in range(70, 81)]

        try:
            if self.mode == ModeEnum.THREAD:
                with ThreadPoolExecutor(self.worker_number) as thread_executor:
                    self.output_list = [f'{item[0]} has port number {item[1]} open' for item in
                                        thread_executor.map(self.scan_port, ips_ports) if item]
            else:
                with ProcessPoolExecutor(self.worker_number) as proc_executor:
                    self.output_list = [f'{item[0]} has port number {item[1]} open' for item in
                                        proc_executor.map(self.scan_port, ips_ports) if item]
        except TimeoutError:
            print('Timeout')
        self.output_results()


if __name__ == '__main__':
    try:
        ip_args = args.ipaddress
        mode = ModeEnum(args.mode) if args.mode else ModeEnum.THREAD
        worker_number = args.number

        start = time.perf_counter()
        if args.function == FunctionEnum.PING.value:
            pinger = IPScannerPing(ip_args, mode, worker_number)
            pinger.do_work()
        elif args.function == FunctionEnum.TCP.value:
            scanner = IPScannerTCP(ip_args, mode, worker_number)
            scanner.do_work()
        end = time.perf_counter()

        if args.verbose:
            print(f'time used: {str(end - start)} seconds')
    except argparse.ArgumentTypeError as err:
        print(err)
    except Exception as err:
        print(err)