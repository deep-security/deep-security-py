# DeepSecurity.py

A unified Python SDK for both SOAP and REST APIs in Deep Security Manager 9.6 and 10.0-10.3. 

*Note: DOES NOT SUPPORT the new REST API in Deep Security Manager 11.1+. Use the new, officially supported Python SDKs instead. See the [Deep Security Automation Center](https://automation.deepsecurity.trendmicro.com/).*

## Support

This is a community project. While you might see contributions from the Deep Security team, there is no official Trend Micro support for this project. The official documentation for the Deep Security APIs is available from the [Deep Security Automation Center](https://automation.deepsecurity.trendmicro.com/). 

Tutorials, feature-specific help, and other information about Deep Security is available from the [Deep Security Help Center](https://help.deepsecurity.trendmicro.com/Welcome.html). 

For Deep Security specific issues, please use the regular Trend Micro support channels. For issues with the code in this repository, please [open an issue here on GitHub](https://github.com/deep-security/deep-security-py/issues).

## History

Deep Security has two APIs that complement each other: a SOAP interface (the classic API), and a REST interface (the new API). Newer functionality is implemented in the REST interface; classic functionality sits in the SOAP API.

As of Deep Security Manager 9.6, most projects using the API are going to interact with both APIs. This SDK presents a unified front so the you don't have to differentiate between the two.

This is the second version of this SDK and it represents a restructuring of how you interact with Deep Security. [v1 is still available](https://github.com/deep-security/deep-security-py/tree/v1.0) in this repository, but should be considered archives.

## Project

The general structure of the SDK is set. We learned a lot in the v1 implementation and have endeavored to make sure that v2+ is simpler to work with while--at the same time--being easier to maintain.

About ~60% of the Deep Security APIs are currently supported in the SDK. The good news is that the areas that are supported are the critical ones to integrating Deep Security into your cloud and hybrid cloud deployments.

## Requirements

Python 2.7 or newer. The project only uses modules in the standard library.

## Usage

```python
import deepsecurity

# 1. Create a manager object and authenticate. Usage via the API mirrors the
#    web administration console for permissions. This defaults to Deep Security
#    as a Service
mgr = deepsecurity.dsm.Manager(username=user, password=pwd, tenant=tenant_name)
#    Create same object against your own Deep Security Manager with a self-signed SSL certificate
mgr = deepsecurity.dsm.Manager(hostname=hostname, username=user, password=pwd, ignore_ssl_validation=True)

# 2. With the object created, you have to authenticate 
mgr.sign_in()

# 3. The Manager() object won't have any data populated yet but does have a number of properties
#    all work in a similar manner
mgr.policies.get()
mgr.rules.get()
mgr.ip_lists.get()
mgr.cloud_accounts.get()
mgr.computer_groups.get()
mgr.computers.get()

# 4. Each of these properties inherits from core.CoreDict which exposes the .get() and other
#    useful methods. .get() can be filtered for various properties in order to reduce the 
#    amount of data you're getting from the Manager(). By default .get() will get all
#    of the data it can. 
#
#    core.CoreDict also exposes a .find() method which is extremely useful for searching
#    for specific objects that meet various criteria. .find() takes a set of keyword arguments
#    that translate to properties on the objects in the core.CoreDict
#
#    For example, this simple loop shows all computers that are currently 'Unmanaged' by 
#    by Deep Security
for computer_id in mgr.computers.find(overall_status='Unmanaged.*'):
  computer = mgr.computers[computer_id]
  print "{}\t{}\t{}".format(computer.name, computer.display_name, computer.overall_status)

#    For example, here's all the computers that are running Windows and have the security
#    policy "Store UI" or "Shipping"
for computer_id in mgr.computers.find(platform='Windows.*', policy_name=['Store UI', 'Shipping']):
  computer = mgr.computers[computer_id]
  print "{}\t{}\t{}".format(computer.name, computer.display_name, computer.overall_status)

#    The .find() method takes uses a regex for string comparison and direct comparison for 
#    other objects. It's extremely flexible and works for all core.CoreDict objects

# 5. You can also take actions on each of these objects. Where it makes sense, the relevant API
#    methods have been added to the object itself.
#
#    For example, if you want to scan a set of computers for malware
mgr.computer[1].scan_for_malware()

#    Apply the same logic for a ComputerGroup
mgr.computer_group[1].scan_for_malware()

#    Of course, you can use the .find() method on all Computers or ComputerGroups to filter the
#    request with a finer granularity
for computer_id in mgr.computers.find(platform='Windows.*', policy_name=['Store UI', 'Shipping']):
  computer = mgr.computers[computer_id]
  computer.scan_for_malware()

#    This applies to any type of scan or action:
#       .scan_for_integrity()
#       .scan_for_recommendations()
#       .assign_policy()
#       ...

# 6. Adding an AWS account is a good example of a unique property for the 
#    environments.CloudAccounts object
mgr.cloud_accounts.add_aws_account(friendly_name, aws_access_key=AWS_ACCESS_KEY, aws_secret_key=AWS_SECRET_KEY)

#    This would add the AWS account and all regions to Deep Security in order to sync 
#    the inventory of EC2 instances automatically
#
#    The IAM identity for the access/secret key needs:
#       - ec2::describeInstances
#       - ec2::describeImages
#       - ec2::describeTags

# 7. Old school but key. API access is the same as a user logging in. If you are going to
#    start a large number of session, you'll need to finish each of them to avoid
#    exception being thrown.
#
#    This function is also called automatically with the object's destructor
mgr.sign_out()
```

## Credentials

In the example about, the credentials were directly passed to the `deepsecurity.dsm.Manager()` object. You can also use a simple configuration file on the local system similar to the AWS CLI to pass credentials to the module. The file should be stored at either;

```
~/.deepsecurity/credentials
# or
C:\Users\USERNAME\.deepsecurity\credentials
```

The file format is very simple;

```
[default]
username = USERNAME
password = PASSWORD
tenant = TENANT NAME
```

Any other lines in the file are currently ignored. When this file exists you can now initialize the `deepsecurity.dsm.Manager()` object without additional parameters being passed.

```python
import deepsecurity
# will use the local configuration file if it exists
mgr = deepsecurity.dsm.Manager()

# will override the local configuration file
mgr = deepsecurity.dsm.Manager(username="NEW USER", password="NEW PASSWORD", tenant="ANOTHER TENANT")
```

### 💥💥💥💥💥 WARNING 💥💥💥💥💥

Storing the credentials on the local disk increases the attack surface for Deep Security. If an attacker were to compromise the local system, they will be able to access Deep Security as a legitimate user. It is critical that you use the role-based access control (RBAC) in Deep Security in order to restrict the permissions granted to the API user to the bare minimum required to complete the intention tasks ([the principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege)).

Think twice before storing the credentials locally. It's not necessarily bad; you just need to be aware of the risk.
