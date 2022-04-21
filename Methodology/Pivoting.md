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

These 2 methods are more than enough

---

## Port Forwarding

## File Transfers

## Listeners

## Methodologies

## Scenarios

