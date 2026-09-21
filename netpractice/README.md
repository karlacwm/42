*This project has been created as part of the 42 curriculum by wcheung.*

## Description
The project is an introduction to the basics of computer networking.
Through getting through exercises on the netpractice server, networking concepts are made practical and visualised.
It is necessary to understand how concepts such as IP address, subnet mask, router, switch, work in order to pass the exercises, and this is the expected learning outcome of this project.

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

These are private IPs:
- from 10.0.0.0 to 10.255.255.255
- from 172.16.0.0 to 172.31.255.255
- from 192.168.0.0 to 192.168.255.255

(Private IPs are reserved strictly for internal, local networks and cannot be routed on the public internet.
This allows millions of different private networks to reuse the exact same IP addresses internally.)

Loopback:
- from 127.0.0.1 to 127.255.255.254

(Loopback address is mostly used for local software testing.
It is a virutal address that always point back to your own machine.)

An IP address consists of two parts: network and host, where the network specifies the network the device belongs to, and the host points to the specific device within that network.
The boundary between these two parts is identified by a subnet mask.

#### Subnet masks
Subnet (sub-network) mask is like a boundary line.
When the computer wants to send a message, it checks the destinatiion.
If the destination is inside its boundary, the message should be sent to a switch.
Else if the destination is outside, the message should be sent to a router.

An IP address is 32 bits long.
A CIDR(Classless Inter-Domain Routing) (e.g. /24) means: the first 24 bits are 1, the rest are 0.
So /24 looks like this: 11111111.11111111.11111111.00000000.
A subnet mask is like a filter on the IP address.
The 1 part is the network, the 0 part is the host(computer's ID).
Computers connected to the same switch must have the exact same network part.

| Subnet Mask |  CIDR |Total IPs | Usable IPs |
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

From the table, it is clear that the no. of total IPs is not the same of usable IPs.
The reason is that the first and last IPs of a network range is always reserved.
First IP is called net prefix, to identify the range and the last one is called broadcast.

One example is, for /30, of the total 4 IP addresses, only 2 are usable:
- net prefix is 255.255.255.252
- first host is 255.255.255.253
- last host is 255.255.255.254
- broadcast is 255.255.255.255

#### Default gateways
In a route, it is indicated with destination => next hop.
Destination is where the data should arrive and next hop is where should the data pass through first, like the first checkpoint or first direction.
A default route actually means 0.0.0.0/0, it means to match 0 bits (/0) from the IP address (0.0.0.0).
Basically it means, to send this out, anywhere else that is not here.
The default gateway is the actual IP address of the router (the next hop) that you hand the packets to.

#### Routers and switches
Routers connect devices from different network, while switches connect devices from the same network.
Therefore, devices conncected by switches has to be in the same network and same subnet mask.
When devices from different routers want to communicate, a route from the device should be specified, and next hop should direct to the local router it is connected to.

#### OSI layers
Open Systems Interconnection (OSI) consists of 7 layers:

|  |  |  |  |
| :---: | :---: | :---: | :---: |
| 7 | application layer | where network applications and end-user processes operate | e.g., HTTP, Web browsers, SSH |
| 6 | presentation layer | translates, encrypts, and formats data so the application layer can understand it |
| 5 | session layer | establishes, maintains, and terminates connections/sessions between applications |
| 4 | transport layer | manages data delivery, error recovery, and flow control | where TCP/UDP protocols and ports operate (**notes)|
| 3 | network layer | handles IP addressing and routes packets across different networks to find the best path | routers live here |
| 2 | data link layer | transfers data between devices on the exact same local network | switches live here |
| 1 | physical layer | the actual hardware: network cables, radio waves, electrical signals, and raw binary data (0s and 1s) |

**(short note: TCP focuses on reliable data delivery, ordered packets and error checks;
whereas UDP, user datagram protocol, focuses on speed and never look back or resend.
so, TCP: unicast(one to one); UDP: broadcast(one to all) and multicast(one to several))

## Resources
Network and subnet masks
[[1]](https://wintelguy.com/ip-mask-visualizer.pl) *\*(very useful calculator/visualisor)\**

Guide
[[1]](http://medium.com/@imyzf/netpractice-2d2b39b6cf0a)
[[2]](https://42-cursus.gitbook.io/guide/4-rank-04/netpractice)
<!-- https://web.archive.org/web/20260225174732/https://42-cursus.gitbook.io/guide/4-rank-04/netpractice/theory
https://web.archive.org/web/20260225174737/https://42-cursus.gitbook.io/guide/4-rank-04/netpractice/level-1-and-2 -->

Youtube
[[1]](https://www.youtube.com/playlist?list=PLIhvC56v63IKrRHh3gvZZBAGvsvOhwrRF)
[[2]](https://www.youtube.com/watch?v=_IOZ8_cPgu8)
[[3]](https://www.youtube.com/watch?v=HQUw0CfQWAM)

Chinese
[[1]](https://learn.microsoft.com/zh-tw/troubleshoot/windows-client/networking/tcpip-addressing-and-subnetting)
[[2]](https://hackmd.io/@ncnu-opensource/book/%2FkEIB82Y2QKCt3U84UoqjFw)
[[3]](https://www.runoob.com/tcpip/tcpip-intro.html)
[[4]](https://www.fortinet.com/tw/resources/cyberglossary/tcp-ip)
[[5]](https://codelove.tw/@tony/post/Zq47ea)
[[6]](https://ihower.tw/cs/networking-tcpip.html)
[[7]](https://medium.com/@bun.coding/u%EF%BD%95%EF%BD%95%E7%B6%B2%E8%B7%AF%E9%80%A3%E6%8E%A5%E6%9C%89%E5%88%86%E5%B1%A4-%E6%B7%BA%E8%AB%87tcp-ip-39364f127bc)
[[8]](https://ithelp.ithome.com.tw/m/articles/10325247)

AI usage:
- help to clarify new concepts and correct me when i understood something wrong
- explain what went wrong when I was stuck at some levels

