# DeepSecurity.py

A unified python SDK for the Deep Security APIs

## History

Deep Security has two APIs that complement each other; one via a SOAP interface (the classic API), and a REST interface (the new API). New functionality is being implemented in the REST interface, classic functionality sits in the SOAP API.

As of version 9.6, most projects using the API are going to interact with both APIs.

This SDK presents a unified front so the development team does not have to differentiate between the two.

## Pre-Requisites

```bash
pip install -r requirements.txt
```

## Usage

```python
import deepsecurity

# Create a manager object and authenticate. Usage via the API mirrors the
# web administration console for permissions
manager = deepsecurity.manager.Manager()
manager.start_session(username=user, password=pass, tenant=tenant_name)

# Is this manager up and running?
print manager.is_up()

# Query the manager for the all policies, groups, and computers
# !!! This can take a while if you have a high number of computers
#     protected
manager.cache_info_locally()

# Print out a quick status of what Deep Security is aware of
print 'ID\tName\tAWS Instance ID\tPlatform\tDeep Security Status\tDeep Security Group'
for computer_id, details in manager.computers.items():
	print '{}\t{}\t{}\t{}\t{}'.format(
		computer_id, 
		details.name, 
		details.cloudObjectInstanceId, 
		details.platform,
		details.overallStatus,
		details.hostGroupName,
		)

manager.finish_session()
```