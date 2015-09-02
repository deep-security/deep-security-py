# DeepSecurity.py

A unified python SDK for the Deep Security APIs

**Work in progress: This SDK is being actively worked on and the current state provides a minimum amount of functionality. Please send a PR if there's something you need ASAP. We'll open up to wider contributions soon**

## History

Deep Security has two APIs that complement each other; one via a SOAP interface (the classic API), and a REST interface (the new API). New functionality is being implemented in the REST interface, classic functionality sits in the SOAP API.

As of version 9.6, most projects using the API are going to interact with both APIs. This SDK presents a unified front so the you don't have to differentiate between the two.

## Pre-Requisites

```bash
pip install -r requirements.txt
```

## Usage

```python
import deepsecurity

# Create a manager object and authenticate. Usage via the API mirrors the
# web administration console for permissions
mgr = deepsecurity.manager.Manager()
mgr.start_session(username=user, password=pwd, tenant=tenant_name)

# Is this manager up and running?
print mgr.is_up()

# Query the manager for the all policies, groups, and computers
# !!! This can take a while if you have a high number of computers
#     protected
mgr.get_all()

# Print out a quick status of what Deep Security is aware of
print 'ID\tName\tAWS Instance ID\tPlatform\tDeep Security Status\tDeep Security Policy'
for comp_id, details in mgr.computers.items():
	print '{}\t{}\t{}\t{}\t{}'.format(
		comp_id, 
		details.hostname, 
		details.cloud_instance_id, 
		details.platform,
		details.status_light,
		details.policy_name,
		)

# Ask all of the current computers to recommend their own security policies
for id, comp in mgr.computers.items():
	comp.scan_for_recommendations()

# Old school but key. API access is the same as a user logging in. If you are going to
# start a large number of session, you'll need to finish each of them to avoid
# exception being thrown
mgr.finish_session()
```