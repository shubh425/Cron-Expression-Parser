# Allowed special characters are asterisk(*), comma(,), dash(-), slash(/)

import re
COLUMN_SIZE = 14

fields = ["minute", "hour", "dayOfMonth", "month", "dayOfWeek", "command"]

labels = {"minute": "minute", "hour": "hour", "dayOfMonth": "day of month", "month": "month", "dayOfWeek": "day of week", "command": "command"}

field_map = {
    "minute": {"label": "minute", "range": [0, 59]},
    "hour": {"label": "hour", "range": [0, 23]},
    "dayOfMonth": {"label": "day of month", "range": [1,31]},
    "month": {"label": "month", "range": [1, 12]},
    "dayOfWeek": {"label": "day of week", "range": [1, 7]}
}

def number_parser(field, value):                                    #function to check whether input is in standard range
    if value.isnumeric():            
        value = int(value)
        low, high = field_map[field]["range"]                       #list unpacking
        if value < low or value > high:                             #if value not in range, raise error
            raise IndexError("Invalid range.")
        return str(value)


def comma_parser(field, value, separator = " "):                    #function to check if there are comma separated values
    if re.match(r"^[0-9]+(,[0-9]+)*$", value):
        parts = value.split(",")
        low, high = field_map[field]["range"]
        for num in parts:
            if int(num) < low or int(num) > high:
                raise IndexError("Invalid range.")
        return separator.join(parts)

def range_parser(field, value):                                     #function to create the range if values separated by '-' 
    if re.match(r"^[0-9]+-[0-9]+$", value):
        low, high = map(int, value.split("-"))
        min,max = field_map[field]["range"]
        output = []
        if low > high:
            while low <= max:
                output.append(str(low))
                low += 1
            
            while min <= high:
                output.append(str(min))
                min += 1
            return " ".join(output)
        else:
            return expand(low, high, field_map[field]["range"])                     #if range already provided in cron string
        

def new_range_parser(field, value):                                     #function to create the range if values separated by '-' 
    if re.match(r"^[0-9]+-[0-9]+/[0-9]+$", value):
        low, high = value.split("-")
        high, step = high.split('/')
        return expand(low,high,field_map[field]["range"],step)
        

def star_parser(field, value):                                      #function to check for '*' in fields, if present use standard range
    if value == "*":
        low, high = field_map[field]["range"]
        return expand(low, high, field_map[field]["range"])


def step_parser(field, value):                                      #function to check for step value to increase start
    if re.match(r"^[*]/[0-9]+$|[0-9]+/[0-9]+$", value):
        start, step = value.split("/")
        low, high = field_map[field]["range"]              #5-45/10    5 15 25 35 45 
        if start != "*":
            low = int(start)
        return expand(low, high, field_map[field]["range"], step)


parsers = [
    number_parser,
    comma_parser,
    range_parser,
    star_parser,
    step_parser,
    new_range_parser
]


def expand(low, high, range=[], step=1):                            #function to expand the range... to be used in range_parser,star_parser,step_parser
    low = int(low)
    high = int(high)
    step = int(step)
    min, max = range

    if low < min or high > max:
        raise IndexError("Invalid range.")                                                
    result = []
    while low <= high:
        result.append(low)
        low += step
    return " ".join(map(str,result))


def formatted_output(parsed, padding=COLUMN_SIZE):                  #function to format the output as per our need
    output = []
    for field in fields:
        output.append(f"{labels[field].ljust(padding)} {parsed[field]}")
    return "\n".join(output)


def parse(cron):                                                    #main function to parse through the cron expression
    if not isinstance(cron, str):
        raise TypeError("Expected a string")
    cron = cron.strip()
    parts = cron.split(" ")
    if len(parts) != 6:
        raise TypeError("Invalid cron format")

    for char in ''.join(parts[:5]):                                  #this block needs to be added in original code
        if char.isalpha() or char in ("~!#$%^&()_?."):
            raise ValueError("Invalid cron format")
    
    command = parts[5]
    parsed = {}
    for idx, field in enumerate(fields):
        value = ""
        if field == "command":
            parsed[field] = command
            continue
        for parser in parsers:
            result = parser(field, parts[idx])
            if result is not None:
                value = result
                break
        parsed[field] = value
    return formatted_output(parsed)


print(parse('5-45/10 0 1,15 */2 5-2 /usr/bin/find'))