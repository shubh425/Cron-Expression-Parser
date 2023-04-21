# Cron-Expression-Parser

## Description
This is a Python module containing a function named parse that is used to parse a cron expression and return a formatted output of the parsed fields.

## Functionality
The 'parse' function takes a cron expression as input and parses it to return a formatted output of the parsed fields. The cron expression is expected to have 6 fields separated by space in the following order:

* minute
* hour
* day of month
* month
* day of week
* command

The function uses regular expressions to parse the fields of the cron expression and returns a formatted output with the labels for each field and its corresponding value.

## Usage
To use the 'parse' function, import it into your Python script and call it with a cron expression as its input parameter:
```
from module_name import parse
result = parse("*/15 0 1,15 * 1-5 /usr/bin/find")
print(result)
```
The above code will output the following formatted string:
```
minute        0 15 30 45
hour          0
day of month  1 15
month         1 2 3 4 5 6 7 8 9 10 11 12
day of week   1 2 3 4 5
command       /usr/bin/find
```
## Notes
* The 'parse' function will raise an error if the input cron expression is not a string or if it does not have exactly 6 fields separated by space.
* The function uses the 'expand' function to expand ranges, which can also be used independently.
* The 'expand' function can raise an error if the input values are not in the specified range.
* The 'formatted_output' function can be used to format any dictionary with the same fields and labels as the parsed dictionary returned by the 'parse' function.
