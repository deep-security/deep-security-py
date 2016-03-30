# DeepSecurity.py

A unified python SDK for the Deep Security APIs

## History

Deep Security has two APIs that complement each other; one via a SOAP interface (the classic API), and a REST interface (the new API). New functionality is being implemented in the REST interface, classic functionality sits in the SOAP API.

As of version 9.6, most projects using the API are going to interact with both APIs. This SDK presents a unified front so the you don't have to differentiate between the two.

This is the second version of this SDK and it represents a restructuring of how you interact with Deep Security. [v1 is still available](https://github.com/deep-security/deep-security-py/tree/v1.0) in this repo but should be considered archival.

## Project

The general structure of the SDK is set. We learned a lot in the v1 implementation and have endeavored to make sure that v2+ is simpler to work with while--at the same time--being easier to maintain.

About ~60% of the Deep Security APIs are currently supported in the SDK. The good news is that the areas that are supported are the critical ones to integrating Deep Security into your cloud and hybrid cloud deployments. Look for rapid progress to bridge the gap with the remaining 40%.

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