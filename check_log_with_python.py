#!/usr/bin/env python3
import sys
import os
import re


def error_search(log_file):
  """
  Function will check log file in attempt to find line with inoutted value
  """
  error = input("What is the error? ")
  returned_errors = []
  with open(log_file, mode='r',encoding='UTF-8') as file:
    for log in  file.readlines():
      error_patterns = []
      for i in range(len(error.split(' '))):
        error_patterns.append(r"{}".format(error.split(' ')[i].lower()))
      if all(re.search(error_pattern, log.lower()) for error_pattern in error_patterns):
        returned_errors.append(log)
  return returned_errors


def file_output(returned_errors):
    """
    Function will write found inoutted lines to the new file
    """
    if not returned_errors:
        print('Nothing was found.')
    else:
        print('Something were found in logs. Please check the file.')
        with open('found_error_ in_logs.log', 'w+') as file:
            for error in returned_errors:
                file.write(error)



if __name__ == "__main__":
  log_file = sys.argv[1]
  print('Log file name = ', log_file)
  returned_errors = error_search(log_file)
  file_output(returned_errors)
  sys.exit(0)
