## General Enumeration

**SMB - 445**

With SMB open we can look for shares that have anonymous access enabled, so that we can view any files inside them that may help us move forward.

``smbmap`` is a great tool to check what shares you have access to, if any.

```bash
smbmap -H <IP> # With No Creds
smbmap -H <IP> -u 'invalid' -p 'invalid'
```

**Useful Commands**

```bash
# SMB Connection
smbclient \\\\<IP>\\<Share> -N # With No Creds
smbclient \\\\<IP>\\<SHARE> -U <USER>%<PASS>
# SMB Enumeration with Credentials
smbmap -H <IP> -d <DOMAIN> -u <USER> -p <PASS> 
```

Appending ``-c 'recurse;ls' `` to the end of an ``smbclient`` command, will recursivly list every item in the entire share, useful for rapidly going through large shares for information.

**FTP - 21**

The File Transfer Protocol is used to transfer files between clients and a server. The most you can really do with this for enumeration is look for anonymous access.

Anonymous FTP Connection

```bash
ftp <IP>
>anonymous
>anonymous
```

**Useful FTP Commands**

```bash
# Download Everything in Directory
> passive
> binary
> prompt off
> mget *
```

## Windows / Active Directory Enumeration

### Important Ports

**LDAP - 389, 636**

With LDAP open we may be able to locate resources such as files and devices in a network. You can also find Domain Names and FQDN's (Fully Qualified Domain Name).

There is an excellent NSE script for ``nmap`` that lets us see all the public information available.

```bash
nmap -n -sV --script "ldap* and not brute" <IP>
```


**MSRPC - 135, 593**

If we have access to RPC, we can use it to get a lot of potentially useful information, including usernames, passwords, domain information.

```bash
rpcclient -U '' -N <IP>
rpcclient -u '<USER>' --password='<PASS>' <IP>
```

**Useful RPC Commands**

```bash
> querydominfo # Domain Information
> enumdomusers # All Domain Users
> enumdomgroups # All Domain Groups
> querydispinfo # Extensive Information On Users
```

I could go on and on, but this article is *insanely* good at helping you get information when you have RPC access. 

- [Enumerating Active Directory with RPC](https://www.hackingarticles.in/active-directory-enumeration-rpcclient/)

### Noteworthy Ports

**WinRM - 5985**

WinRM, or "Windows Remote Management" and is a service that lets Admin's perform management tasks on systems remotely. It's sort of like SSH.

If the service is open and you have a valid pair of credentals you found somwhere, maybe they were for SMB or maybe you found them by enumerating RPC, Always Check to see if you can login using ``evil-winrm`` to get a shell. If you get your hands on an NT hash, try connecting with it too.

```bash
evil-winrm -i <IP> -u '<USER>' -p '<PASS>' # Using Creds
evil-winrm -i 10.10.10.192 -u '<USER>' -H '<NTML_HASH>' # Using NTML Hash
```
