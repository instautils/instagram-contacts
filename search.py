# -*- coding: utf-8 -*-
#!/bin/python

import json
from instagram import Instagram
import sys

with open("conf.json") as configfile:
    config = json.loads(configfile.read())
    
insta = Instagram(config["username"],config["password"])
if not insta.login():
    print "Login failed [" + json.loads(insta.lastResponse.text)["message"] + "]"
    sys.exit(-1)

numbers = [line.rstrip('\n') for line in open('numbers.txt')]
    
contacts = []
for number in numbers :
    contact = {}
    contact["phone_numbers"] = [number]
    contact["first_name"] = number
    contact["email_addresses"] = []
    contacts.append(contact)

if insta.syncFromAdressBook(contacts):
    result = insta.lastJson
    if result["status"] != "ok":
        print "Syncing contacts failed " + result["status"]
        sys.exit(-3)
        
    for item in result["items"]:
        try:
            print item["user"]["extra_display_name"] + " = " + item["user"]["username"]
        except:
            print "UNKNOWN NUMBER = " + item["user"]["username"]
else:
    print "Faild to get contacts [" + json.loads(insta.lastResponse.text)["message"] + "]"
    sys.exit(-2)
