#!/usr/bin/env python3
import sys
import re
import operator
import csv

#init dictionaries
per_user = {}
errors = {}

#reading file log line by line
with open('syslog.log') as file:
    for item in file.readlines():
        match_groups_reg_exp = re.search(r"ticky: ([\w+]*):? ([\w' ]*)[\[[#0-9]*\]?]? ?\((.*)\)$", item)
        debug_level, error_msg, user = match_groups_reg_exp.group(1), match_groups_reg_exp.group(2), match_groups_reg_exp.group(3)
        # Add new user to dict if not exists
        if user not in per_user.keys():
            per_user[user] = {}
            per_user[user]['INFO'] = 0
            per_user[user]['ERROR'] = 0
        # Populates per_user dict with users logs entry
        if debug_level == 'INFO':
            per_user[user]["INFO"] += 1
        elif debug_level == 'ERROR':
            per_user[user]['ERROR'] += 1

        # Error message dict
        if error_msg not in errors.keys():
            errors[error_msg] = 1
        else:
            errors[error_msg] += 1

#Sorting dictionaries
sorted_per_user = {k: per_user[k] for k in sorted(per_user)}
sorted_errors = {k: v for k, v in sorted(errors.items(), key=lambda item: item[1], reverse=True)}

file.close() #file close

#User stat CSV
with open('user_statistics.csv', 'w', newline='') as csv_user_stat:
    fieldnames = ['Username', 'INFO', 'ERROR']
    csv_inst = csv.DictWriter(csv_user_stat, fieldnames=fieldnames)
    csv_inst.writeheader()
    for user in sorted_per_user:
       csv_inst.writerow({'Username': user, 'INFO': sorted_per_user[user]['INFO'], 'ERROR': sorted_per_user[user]['ERROR']})

#Error_message CSV
with open('error_message.csv', 'w', newline='') as csv_error:
    fieldnames = ['Error', 'Count']
    csvw = csv.DictWriter(csv_error, fieldnames=fieldnames)
    csvw.writeheader()
    for key, value in sorted_errors.items():
       csvw.writerow({'Error': key, 'Count': value})
