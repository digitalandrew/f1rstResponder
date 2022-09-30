from ast import arg
import logging.handlers
import logging
import socket
import getopt
import sys
import random
import string
import time
from impacket.smbconnection import SMBConnection
import impacket.smb3

def main():

    opts, args = getopt.getopt(sys.argv[1:], "n:f:l:u:p:d:s:h", [
                               'name', 'frequency', 'logserver', 'user', 'password', 'domain','sysport'])
    hflag = False
    nflag = False
    fflag = False
    lflag = False
    uflag = False
    pflag = False
    dflag = False
    sflag = False
    PORT = 445  # Have to use 445 or else responder will not do LLMNR NTBIOS poisoning
    domain =''

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

        if opt == '-u':
            username = arg
            uflag = True

        if opt == '-p':
            password = arg
            pflag = True
        
        if opt == '-d':
            domain = arg
            dflag = True
        if opt == '-s':
            sysport = arg
            sflag == True

        elif opt == '-h':
            print()
            print("***** f1rstResponder *****")
            print()
            print("Usage example: f1rstResponder.py -n lookup_name -f 4 -l 192.168.121.5")
            print()
            print("Flags:")
            print(
                "-n           Set name to query, if no name is set a random string will be used")
            print(
                "-f           Set frequency per hour to query, if not set will default to 4/hr")
            print(
                "-l           Toggle logging to syslog and set IP of remote syslog server")
            print(
                "-s           Set the port of the syslog server, if not set will default to 514")
            print(
                "-u           Username to use to connect back to responder fake SMB share")
            print(
                "-p           Password to use to connect back to responder fake SMB share")
            quit()

    if (uflag == True and pflag == False) or (uflag == False and pflag == True):
        print("You must enter both a username and password or neither.")
        exit()

    if nflag == True:
        HOST = name  # The fake host name that will trigger DNS, LLMNR and NTBIOS lookup
    elif nflag == False:  # Generate random string to use as name to try and resolve
        letters = string.ascii_lowercase
        randstr = ''.join(random.choice(letters) for i in range(8))
        HOST = randstr

    if fflag == False:  # Set freq to default of 4/hr
        freq = 4

    sleeptimer = (60 / freq) * 60

    if sflag == False:
        sysport = 514

    if lflag == True:
        logger = logging.getLogger('MyLogger')
        logger.setLevel(logging.DEBUG)
        handler = logging.handlers.SysLogHandler(address=(logserver, sysport))
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

            if (pflag == True and uflag == True):
                print(
                    f"Attempting to connect back to {ip[0]} with username: {username} and password: {password}")
                try:
                    smbClient = SMBConnection(
                        ip[0], ip[0], sess_port=int(PORT))
                    smbClient.login(username, password, domain)

                except (impacket.smb3.SessionError, impacket.smbconnection.SessionError) as e:
                    "Connection attempt successful, username and hash passed"
                    pass

            if lflag == True:
                logger.warning(
                    f"f1rstResponder request to {HOST} responded to by {ip[0]} - indication of potential poisioned response by Responder")
                if uflag == True and pflag == True:
                    logger.warning(
                    f"username: {username} and password: {password} as a hash passed to suspected responder smbshare at IP {ip[0]}")

        except socket.gaierror:  # If we get a gaierror the name cannot resolve
            print(f"f1rstResponder request to {HOST} with no response")
            if lflag == True:
                logger.info(
                    f"f1rstResponder request to {HOST} with no response")
            pass
        time.sleep(sleeptimer)


if __name__ == '__main__':
    main()
