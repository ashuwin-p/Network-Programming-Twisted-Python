# Network-Programming-Twisted-Python
# Networking Protocol Implementations

This repository contains a series of exercises focused on the implementation of various networking protocols. Each exercise is implemented in Python and uses the Twisted framework for network programming.

## Table of Contents

- [EX10 - Implementation of Stop and Wait Protocol](#ex10---implementation-of-stop-and-wait-protocol)
- [EX11 - Implementation of HTTP Web Client](#ex11---implementation-of-http-web-client)
- [EX12 - Implementation of Remote Procedural Call (RPC)](#ex12---implementation-of-remote-procedural-call-rpc)
- [EX13 - Implementation of Subnetting](#ex13---implementation-of-subnetting)
- [EX14 - Implementation of DNS, SMTP, and SNMP](#ex14---implementation-of-dns-smtp-and-snmp)
- [EX16 - Implementation of Routing Protocols](#ex16---implementation-of-routing-protocols)
  - [Distance Vector Routing](#distance-vector-routing)
  - [Flooding](#flooding)
  - [Link State Routing](#link-state-routing)

## EX10 - Implementation of Stop and Wait Protocol

This exercise demonstrates the implementation of the Stop and Wait protocol for reliable data transmission. The protocol ensures that each packet is acknowledged before the next one is sent, providing a simple form of flow control.

- **File:** `ex10_stop_and_wait.py`

## EX11 - Implementation of HTTP Web Client

This exercise involves creating an HTTP web client that can send GET requests to a web server and display the response. It demonstrates basic HTTP communication using the Twisted framework.

- **File:** `ex11_http_webclient.py`

## EX12 - Implementation of Remote Procedural Call (RPC)

This exercise implements a basic RPC mechanism using Twisted's Perspective Broker (PB). It allows clients to call remote methods on a server as if they were local, facilitating distributed computing.

- **File:** `ex12_rpc.py`

## EX13 - Implementation of Subnetting

This exercise involves calculating and displaying subnet information based on a given IP address and subnet mask. It includes the calculation of the number of subnets, the number of hosts per subnet, and the range of IP addresses in each subnet.

- **File:** `ex13_subnetting.py`

## EX14 - Implementation of DNS, SMTP, and SNMP

This exercise demonstrates the implementation of three different protocols:
- **DNS:** Resolves domain names to IP addresses.
- **SMTP:** Simple Mail Transfer Protocol for sending emails.
- **SNMP:** Simple Network Management Protocol for network management.

- **File:** `ex14_dns_smtp_snmp.py`

## EX16 - Implementation of Routing Protocols

This exercise covers the implementation of various routing protocols:

### Distance Vector Routing

Implements the Distance Vector Routing protocol, where each router shares its routing table with its neighbors and updates its table based on the received information to find the shortest path.

- **File:** `ex16_distance_vector_routing.py`

### Flooding

Implements the Flooding protocol, where each incoming packet is transmitted through every outgoing link except the one it arrived on, ensuring that the packet reaches all parts of the network.

- **File:** `ex16_flooding.py`

### Link State Routing

Implements the Link State Routing protocol, where each router constructs a map of the connectivity of the network in the form of a graph and then uses Dijkstra's algorithm to calculate the shortest path to each node.

- **File:** `ex16_link_state_routing.py`

## Getting Started

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/networking-protocols.git
   cd networking-protocols
