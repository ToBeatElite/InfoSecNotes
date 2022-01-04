## Notes On Kerberoasting

**Intro - Kerberos Protocol**

Kerberos is a *Network Authentication Protocol*. It makes use of *tickets* to verifying identities and enabling trusted communications in a network. By default, Kerberos uses UDP port 88. Its often used in Active Directory Environments.

<img src='https://www.redsiege.com/wp-content/uploads/2020/10/auth.png'>

**What is Kerberoasting?**

Kerberoasting is an attack that allows an attacker to take advantage of how service account leverage and use Kerberos authentication with *Service Principal Names (SPN)*. If the attack is successful, you end up getting hashes of the service account. It does not *exploit* any security loophole, instead you are literally just *abusing* an intended functionality of Kerberos. This attack makes use of the "TGS" Portion of the Kerberos Protocol.

**What are SPN's?**

*Service Principal Names* are unique identifier's of a service instance. Kerberos uses SPN's to associate a service instance to a service account. This lets a client request and use a service, without knowing the actual account its being ran on.

**How does Kerberoasting Work?**

When we Kerberoast, we are locating Users on the Domain that have *SPN's* tied to them, request a TGS ticket, and creating a crackable hash from the response.

The attack is done as follows:

- Send ``TGS-REQ`` to the ``KDC`` for any account that has an *SPN* tied to it. 
- Receive the ``TGS-REP``

The ``TGS-REP`` will be encrypted with the NTLM Hash of the account the *SPN* is tied to, and so we can use the response to get the hash out of it, which we can then crack offline.

**When is Kerberoasting Effective?**

You can only Kerberoast when you have compromised a user on a domain, so it's a good idea to try this attack when you're trying to pivot to a higher privileged account, as service accounts are often misconfigured to be given more power than they would need. Furthermore, you don't need a privileged  account to do this attack, any old domain user is fine.

**Mitigation**

Kerberoasting can never be fully patched, because, as stated previously, there is nothing being exploited and only abused. You should set very strong passwords for all users with *SPN's* tied to them, and rotate these passwords regularly. In addition to this, do not give your service accounts more privileges than they need, keep their privileges to a minimum.


**Resources**

- [How to Prevent Kerberoasting Attacks](https://www.lepide.com/blog/how-to-prevent-kerberoasting-attacks/)
- [Attacking Active Directory - Kerberoasting](https://www.youtube.com/watch?v=-3MxoxdzFNI)
- [QOMPLX Knowledge: Kerberoasting Attacks Explained](https://www.qomplx.com/qomplx-knowledge-kerberoasting-attacks-explained/)
- Lot's more; there is so much on the Internet on Kerberoasting.
