#!/usr/bin/env python
###########################################################################################
# File: server_monitor.py
# Name: Server Monitor
# Description: Performs healthcheck on a server, and notifies by e-mail if issue ocurrs. 
# Version: 0.1
###########################################################################################

# Load modules for HTTP(S) and TCP connections, and I/O arguments.
from os import system
from urllib2 import urlopen
from socket import socket
from sys import argv
from time import asctime

# Help menu. 
def usage():
    print('%s <test-type> <server-info> <email-address>\n' % (argv[0]))
    print('\ttest-type    \ttcp or http')
    print('\tserver-info  \thostname:port for tcp')
    print('\t             \thttp://hostname/page for http')
    print('\temail-address\tusername or username@domain.com\n')

# Establish a TCP connection to hostname:port, and report if attempt was successfull.
def tcp_test(server_info):
    cpos = server_info.find(':')
    if cpos < 1 or cpos == len(server_info) - 1:
        print('You need to give server info as hostname:port.')
        usage()
        return True
    try:
        sock = socket()
        sock.connect((server_info[:cpos], int(server_info[cpos+1:])))
        sock.close
        return True
    except:
        return False

# Establish a HTTP(S) request to a server, and report if attempt was successfull.
def http_test(server_info):
    try:
        data = urlopen(server_info).read()
        return True
    except:
        return False

# Parse arguments passed from the script, and determine which test was requested.
def server_test(test_type, server_info):
    if test_type.lower() == 'tcp':
        return tcp_test(server_info)
    elif test_type.lower() == 'http':
        return http_test(server_info)
    else:
        print('Invalid test-type given, please use either tcp or http.')
        return True

# Create e-mail message, and send notification.
def send_error(test_type, server_info, email_address):
    subject = '%s: %s %s is down' % (asctime(), test_type.upper(), server_info)
    message = 'Server Monitor: Performed a health-check running a %s test against %s. The server is down.' % (test_type.upper(), server_info)
    system('echo "%s" | mail -s "%s" %s' % (message, subject, email_address))

# Main method - Invoke script and parse arguments. 
if __name__ == '__main__':
    if len(argv) != 4:
        print('Wrong number of arguments.')
        usage()
    elif not server_test(argv[1], argv[2]):
        send_error(argv[1], argv[2], argv[3])