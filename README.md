# f1rstResponder

## About
f1rstResponder is designed to act as a honeypot for instances of responder running on a network. It attempts to connect to bad hostnames on the network and listens for a DNS, MDNS, or LLMNR response that resolves the bad hostnames, this gives an indication of responder poisoning responses. 

Optionally, f1rstResponder can be configured to connect to preconfigured bad hostnames (such as something that would match a common typo on your network) and it can also be configured to send logs to an external syslog server. 

## Useage:

There are two useage options, f1rstResponder can be run as a standalone python script or as a docker container.

### Python Script

Useage Example:

`f1rstResponder.py -n name_of_host -f 10 -l 192.168.1.11`

Optional Arguments:

-n &nbsp; Set the name of the host to look up, if this is not set a random 8 character string will be used  
-f &nbsp; Set the frequency that f1rstResponder will attempt to connect to the host, if this is not set it will default to 4/hr  
-l &nbsp; Toggle on syslog logging and set the IP address of the syslog server  

### Docker Container

Clone the repo:

`git clone https://github.com/digitalandrew/f1rstResponder`

Build the docker container

`sudo docker build -t f1rstresponder .`

Run the docker container with your desired arguments:

`docker run -it  --rm f1rstresponder -n name_of_host -f 10 -l 192.168.1.11`







