*This project has been created as part of the 42 curriculum by wcheung.*

## Description
The project is an introduction to the basics of computer networking.
Through getting through exercises on the netpractice server, networking concepts are made practical and visualised.
It is necessary to understand how concepts such as IP address, subnet mask, router, switch etc work in order to pass the exercises, and this is the expected learning outcome of this project.

## Instruction
First, download the "net_practice" package from intra.

Go to the directory:
```
cd /net_practice.1.9/net_practice/
```

Then, run:
```
./run.sh
```

The netpractice server should run in a browser, if not, open a browser with:
```
http://0.0.0.0:49152/
```

There are two modes: training and evaluation.
The json files in repo are from the 10 levels in training mode.
After completing each level, the option "get my config" was used to save my config in json format.
During evaluation, we run evaluation mode to get 3 random levels.

## Concepts explained
#### TCP/IP addressing
TCP stands for Transmission Control Protocol and IP for Internet Protocol.
TCP is the protocal that breaks data into smaller pieces to send them over the network.
It works with IP address which helps to identify the device connected to a network, in simple words, where the data should be sent to.

There are private IPs:
- from 10.0.0.0 to 10.255.255.255
- from 172.16.0.0 to 172.31.255.255
- from 192.168.0.0 to 192.168.255.255
- from 127.0.0.1 to 127.255.255.254

#### Subnet masks
Subnet (sub-network) is like a boundary line.
When the computer wants to send a message, it checks the destinatiion.
If the destination is inside its boundary, it sends the message to a switch.
Else if the destination is outside, it sends the message to a router.

An IP address is 32 bits long.
A CIDR(Classless Inter-Domain Routing) like /24 means: the first 24 bits are 1, the rest are 0.
So /24 looks like this: 11111111.11111111.11111111.00000000.
A subnet mask is like a filter on the IP address.
The 1 part is the network, the 0 part is the host(computer's ID).
Computers connected to the same switch must have the exact same network part.

| CIDR | Subnet Mask | Total IPs | Usable IPs |
| :---: | :--- | :---: | :--- |
| `255.255.255.255` | /32 | 1 | 1 |
| `255.255.255.254` | /31 | 2 | 2 |
| `255.255.255.252` | /30 | 4 | 2 |
| `255.255.255.248` | /29 | 8 | 6 |
| `255.255.255.240` | /28 | 16 | 14 |
| `255.255.255.224` | /27 | 32 | 30 |
| `255.255.255.192` | /26 | 64 | 62 |
| `255.255.255.128` | /25 | 128 | 126 |
| `255.255.255.0` | /24 | 256 | 254 |
| `255.255.254.0` | /23 | ... | ... |
| `255.255.252.0` | /22 | ... | ... |
| `255.255.248.0` | /21 | ... | ... |
| `255.255.240.0` | /20 | ... | ... |
| `255.255.224.0` | /19 | ... | ... |
| `255.255.192.0` | /18 | ... | ... |
| `255.255.128.0` | /17 | ... | ... |
| `255.255.0.0` | /16 | ... | ... |
| ... | ... | ... | ... |


#### Default gateways
In a route, it is indicated with destination => next hop.
Destination is where the data should arrive and next hop is where should the data pass through first, like the first checkpoint or first direction.
A default gateway actually means 0.0.0.0/0, it means to match 0 bits (/0) from the IP address (0.0.0.0).
Basically it means, to send this out, anywhere else that is not here.

#### Routers and switches
Routers connect devices from different network, while switches connect devices from the same network.
Therefore, devices conncected by switches has to be in the same network and same subnet mask.
When devices from different routers want to communicate, a route from the device should be specified, and next hop should direct to the local router it is connected to.

#### OSI layers
Open Systems Interconnection (OSI) consists of 7 layers:

|  |  |
| :---: | :--- |
| layer 7 | application layer |
| layer 6 | presentation layer |
| layer 5 | session layer |
| layer 4 | transport layer |
| layer 3 | network layer |
| layer 2 | data link layer |
| layer 1 | physical layer |


## Resources
Network and subnet masks
[[1 *\*(very useful calculator/visualisor)\**]](https://wintelguy.com/ip-mask-visualizer.pl)

Guide
[[1]](http://medium.com/@imyzf/netpractice-2d2b39b6cf0a)
[[2]](https://42-cursus.gitbook.io/guide/4-rank-04/netpractice)
<!-- https://web.archive.org/web/20260225174732/https://42-cursus.gitbook.io/guide/4-rank-04/netpractice/theory
https://web.archive.org/web/20260225174737/https://42-cursus.gitbook.io/guide/4-rank-04/netpractice/level-1-and-2 -->

Youtube
[[1]](https://www.youtube.com/playlist?list=PLIhvC56v63IKrRHh3gvZZBAGvsvOhwrRF)
[[2]](https://www.youtube.com/watch?v=_IOZ8_cPgu8)
[[3]](https://www.youtube.com/watch?v=HQUw0CfQWAM)

AI usage:
- help to clarify new concepts and correct me when i understood something wrong
- explain what went wrong when I was stuck at some levels

