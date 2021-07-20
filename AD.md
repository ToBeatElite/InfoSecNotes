# Active Directory

## Enumeration

Nmap: `sudo nmap -n -sV --script "ldap* and not brute" <IP>`

Enum4Linux: `enum4linux <IP>`

Kerbrute: `./kerbrute userenum -d <Domain Controller> --dc <Target IP> /<Wordlst>`

GetNPUsers: `sudo python3 GetNPUsers.py <Domain Controller>/<Valid Username> -no-pass`



add secretsdump
add ticket attacks

 
