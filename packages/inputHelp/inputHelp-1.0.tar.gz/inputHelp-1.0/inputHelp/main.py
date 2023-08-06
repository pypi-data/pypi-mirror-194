'''
Module
  inputHelp
Vesion
  2.0
Author
  c20h12untitled

Contains functions to validate input for command line programs
'''


def _convertInput(prompt, failedText, conversionFn):
  '''
  attempts to convert the input to a desired type, retries if it is not successful
  PARAMETERS
    prompt: str - prompt for input
    failedText: str - text to print when the conversion fails
    conversionFn: function - a type constructor to call on the input
  RETURNS
    conversionFn() - the converted result
  '''
  res = input(prompt)
  while True:
    try:
      return conversionFn(res)
    except ValueError:
      print(failedText)
      res = input(prompt)

# functions to get the input and return the converted type
def getNumber(type, prompt,
             failedText="Input is not a integer!", 
             range=(-float("inf"), float("inf")),
             outOfRangeText="Input is out of accepted range!"):
  while not range[0] <= \
           (result := _convertInput(prompt, failedText, type))\
           <= range[1]:
    print(outOfRangeText)
  return result

def getBool(prompt, failedText="Input is not a bool!", trueValue='True', falseValue='False'):
  return _convertInput(prompt, failedText, lambda t: True if t == trueValue else falseValue)

def getString(prompt, filter=None, failedText="Input is invalid!", emptyText="Input is empty!"):
  '''
  attempt to get a string with constraints, retries if input does not match the restrains
  PARAMETERS
    prompt: str - the prompt for input
    filter: str | tuple - A string is used for exact matches,
        a tuple of values can be used to set restrictions, 
    failedText: str - text to print if the input does not match
    emptyText: str - text to print if input is empty
  RETURNS
    str - the input gotted
  '''
  res = input(prompt)
  if not filter:
    while res == '':
      print(emptyText)
      res = input(prompt)
    return res
  elif type(filter) == tuple:
    while res not in filter:
      print(failedText)
      res = input(prompt)
  elif type(filter) == str:
    while res != filter:
      print(failedText)
      res = input(prompt)
  return res

import re
def getStringRegex(prompt, filter, failedText="Input does not match the pattern!"):
  '''
  attempt to get a string with a regex filter, retries if input does not match the restrains
  PARAMETERS
    prompt: str - the prompt for input
    filter: str - the regular expression (a raw string)
    failedText: str - text to print if the input does not match
  RETURNS
    str
  '''
  while not re.match(filter, res := input(prompt)):
    print(failedText)
  return res
