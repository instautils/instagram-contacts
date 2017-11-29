# -*- coding: utf-8 -*-
# !/bin/python

import json
from instagram.instagram import Instagram
import sys
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-u", "--username", required=True, help="Instagram username")
ap.add_argument("-p", "--password", required=True, help="Instagram password")
ap.add_argument("-c", "--contacts", required=True, help="Contacts list in txt file")

# TODO : add infinite option

args = vars(ap.parse_args())

insta = Instagram(args["username"], args["password"])
if not insta.login():
    print "Login failed [" + json.loads(insta.lastResponse.text)["message"] + "]"
    sys.exit(-1)

numbers = [line.rstrip('\n') for line in open(args["contacts"], 'r')]

contacts = []
for number in numbers:
    contact = dict()
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
        except KeyError:
            print "UNKNOWN NUMBER = " + item["user"]["username"]
else:
    print "Failed to get contacts [" + json.loads(insta.lastResponse.text)["message"] + "]"
    sys.exit(-2)
