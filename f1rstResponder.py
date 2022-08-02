from ast import arg
import logging.handlers
import logging
import socket
import getopt
import sys
import random
import string
import time


def main():

    opts, args = getopt.getopt(sys.argv[1:], "n:f:l:h", [
                               'name', 'frequency', 'logserver'])
    hflag = False
    nflag = False
    fflag = False
    lflag = False
    for opt, arg in opts:
        if opt == '-n':
            name = arg
            nflag = True
        if opt == '-f':
            freq = arg
            try:
                int(freq)
            except ValueError:
                print("Invalid frequency, select a number between 1-60")
                quit()
            freq = int(freq)
            if freq < 1 or freq > 60:
                print("Invalid frequency, select a number between 1-60")
                quit()
            fflag = True
        if opt == '-l':
            logserver = arg
            lflag = True
        elif opt == '-h':
            print()
            print("***** f1rstResponder *****")
            print()
            print("Usage example: f1rstResponder.py -n lookup_name -f 4 -r 192.168.121.5")
            print()
            print("Flags:")
            print(
                "-n           Set name to query, if no name is set a random string will be used")
            print(
                "-f           Set frequency per hour to query, if not set will default to 4/hr")
            print(
                "-l           Toggle logging to syslog and set IP of remote syslog server")
            quit()
    if nflag == True:
        HOST = name  # The fake host name that will trigger DNS, LLMNR and NTBIOS lookup
    elif nflag == False:  # Generate random string to use as name to try and resolve
        letters = string.ascii_lowercase
        randstr = ''.join(random.choice(letters) for i in range(8))
        HOST = randstr
    PORT = 445  # Have to use 445 or else responder will not do LLMNR NTBIOS poisoning
    if fflag == False:  # Set freq to default of 4/hr
        freq = 4

    sleeptimer = (60 / freq) * 60

    if lflag == True:
        logger = logging.getLogger('MyLogger')
        logger.setLevel(logging.DEBUG)
        handler = logging.handlers.SysLogHandler(address=(logserver, 514))
        logger.addHandler(handler)
        logger.info(f"f1rstResponder starting connection attempts to {HOST}")

    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f"f1rstResponder attempting connection to {HOST}")
            # Attempt to open socket on hostname and port, will throw error if name cannot resolve
            s.connect((HOST, PORT))
            ip = s.getpeername()
            print(
                f"f1rstResponder request to {HOST} responded to by {ip[0]} - indication of potential poisioned response by Responder")
            if lflag == True:
                logger.warning(
                    f"f1rstResponder request to {HOST} responded to by {ip[0]} - indication of potential poisioned response by Responder")
        except socket.gaierror:  # If we get a gaierror the name cannot resolve
            print(f"f1rstResponder request to {HOST} with no response")
            if lflag == True:
                logger.info(
                    f"f1rstREsponder request to {HOST} with no response")
            pass
        time.sleep(sleeptimer)


if __name__ == '__main__':
    main()
