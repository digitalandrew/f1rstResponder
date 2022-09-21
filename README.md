# f1rstResponder

## About
f1rstResponder is designed to act as a honeypot for instances of responder running on a network. It attempts to connect to bad hostnames on the network and listens for a DNS, MDNS, or LLMNR response that resolves the bad hostnames, this gives an indication of responder poisoning responses.

Optionally, f1rstResponder can be configured to connect to preconfigured bad hostnames (such as something that would match a common typo on your network) and it can also be configured to send logs to an external syslog server.

If passed a username AND password f1rstResponder will attempt to connect back to the malicious smb share hosted by responder. This provides an opportunity to tie an AD Deception account into the responder alerting as the account name and hash will then be intercepted by responder and most likely relayed or used by the adversary. Additional monitoring and restrictions can be placed on this AD deception account and combined with the f1rstResponder alert to allow for a zero false positive alert of an intruder in the network. 
 

## Useage:

There are two useage options, f1rstResponder can be run as a standalone python script or as a docker container.

### Python Script

Useage Example:

`f1rstResponder.py -n name_of_host -f 10 -l 192.168.1.11`

Optional Arguments:

-n &nbsp; Set the name of the host to look up, if this is not set a random 8 character string will be used  
-f &nbsp; Set the frequency that f1rstResponder will attempt to connect to the host, if this is not set it will default to 4/hr  
-l &nbsp; Toggle on syslog logging and set the IP address of the syslog server

-u &nbsp; Set the username to be used to connect back to the responder malicious smb share

-p &nbsp; Set the password to be used to connect back to the responder malicious smb share

-d &nbsp; Set the domain to be used to connect back to the responder malicious smb share

### Docker Container

Clone the repo:

`git clone https://github.com/digitalandrew/f1rstResponder`

Build the docker container

`sudo docker build -t f1rstresponder .`

Run the docker container with your desired arguments:

`docker run -it  --rm f1rstresponder -n name_of_host -f 10 -l 192.168.1.11`







