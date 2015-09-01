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