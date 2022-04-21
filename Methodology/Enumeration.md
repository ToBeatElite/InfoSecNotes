## General Enumeration

**SMB - 445**

With SMB open we can look for shares that have anonymous access enabled, so that we can view any files inside them that may help us move forward.

``smbmap`` is a great tool to check what shares you have access to, if any. Try all of these, they can yeild different results

```bash
smbmap -R -H <IP> # With No Creds
smbmap -R -H <IP> -u 'invalid'
smbmap -R -H <IP> -u 'invalid' -p 'invalid'
```

**Useful Enumeration Commands**

```bash
# SMB Connection
smbclient \\\\<IP>\\<Share> -N # With No Creds
smbclient \\\\<IP>\\<SHARE> -U <USER>%<PASS>
# SMB Enumeration with Credentials
smbmap -R -H <IP> -d <DOMAIN> -u <USER> -p <PASS> 
```

Appending ``-c 'recurse;ls' `` to the end of an ``smbclient`` command, will recursivly list every item in the entire share, useful for rapidly going through large shares for information.

**Useful SMB Commands**

```bash
# Download Everything in Directory

> prompt off
> mget *
```

**FTP - 21**

The File Transfer Protocol is used to transfer files between clients and a server. The most you can really do with this for enumeration is look for anonymous access.

Anonymous FTP Connection

```bash
ftp <IP>
> anonymous
> anonymous
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

You can query LDAP to get lots of imformation on a Domain. Usernames, Groups, Domain Names, etc etc. Somtimes there are passwords or other confidential information inside the data and you can access it. ``ldapsearch`` is a great tool to make these queries.

```bash
ldapsearch -x -H ldap://<IP> -b '<BASEDN>'

# Examples

ldapsearch -x -H ldap://10.10.10.182 -b 'DC=cascade,DC=local'
ldapsearch -x -H ldap://10.10.10.6 -b 'CN=Joe Clark,OU=it,DC=evilcorp,DC=local'
```

These are some other tools you may want to use.

An excellent NSE script for ``nmap`` that lets us see the anonymous information available.

```bash
nmap -Pn -p 389 -sV --script "ldap* and not brute" <IP>
```

You can use [ldapdomaindump](https://github.com/dirkjanm/ldapdomaindump) to get an overview of users, groups, computers, policies in the domain. You will get better results with credentials, rarely is anonymous access allowed.

```bash
ldapdomaindump <IP>

# With Authentication 
ldapdomaindump -u '<DOMAIN>\<USER>' -p '<PASS>' <IP> -o ./ldapdump
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
evil-winrm -i 10.10.10.192 -u '<USER>' -H '<NT_HASH>' # Using NT Hash
```

**Kerberos - 88**

having Kerberos present means that its a DC. you can do AD Attacks like Kerberoasting or AS REP Roasting; this port should be noted but there is nothing to really enumerate from it.
