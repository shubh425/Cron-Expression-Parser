import re
COLUMN_SIZE = 14

fields = ["minute", "hour", "dayOfMonth", "month", "dayOfWeek", "command"]

labels = {"minute": "minute", "hour": "hour", "dayOfMonth": "day of month", "month": "month", "dayOfWeek": "day of week", "command": "command"}

field_map = {
    "minute": {"label": "minute", "range": [0, 59]},
    "hour": {"label": "hour", "range": [0, 23]},
    "dayOfMonth": {"label": "day of month", "range": [1, 31]},
    "month": {"label": "month", "range": [1, 12]},
    "dayOfWeek": {"label": "day of week", "range": [1, 7]}
}

def number_parser(field, value):                                    #function to check whether input is in standard range
    if not value.isnumeric():
        return None
    value = int(value)
    low, high = field_map[field]["range"]
    if value < low or value > high:
        raise IndexError("Invalid range.")
    return str(value)


def comma_parser(field, value, separator = " "):                    #function to check if there are comma separated values
    if re.match(r"^[0-9]+(,[0-9]+)*$", value):
        parts = value.split(",")
        return separator.join(parts)


def range_parser(field, value):                                     #function to create the range if values separated by '-' 
    if re.match(r"^[0-9]+-[0-9]+$", value):
        low, high = map(int, value.split("-"))
        return expand(low, high, field_map[field]["range"])


def star_parser(field, value):                                      #function to check for '*' in fields, if present use standard range
    if value == "*":
        low, high = field_map[field]["range"]
        return expand(low, high, field_map[field]["range"])


def step_parser(field, value):                                      #function to check for step value to increase start
    if '/' in value:
        start, step = value.split("/")
        low, high = field_map[field]["range"]
        if start != "*":
            low = int(start)
        return expand(low, high, field_map[field]["range"], step)


parsers = [
    number_parser,
    step_parser,
    comma_parser,
    range_parser,
    star_parser,
]


def expand(low, high, range=[], step=1):
    low = int(low)
    high = int(high)
    step = int(step)
    if low > high:
        return []
    min, max = range
    result = []
    current = low
    while current <= high:
        if (min is not None and current < min) or (max is not None and current > max):
            raise IndexError("Invalid range.")
        result.append(current)
        current += step
    return " ".join(map(str,result))


def formatted_output(parsed, padding=COLUMN_SIZE):
    output = []
    for field in fields:
        output.append(f"{labels[field].ljust(padding)} {parsed[field]}")
    return "\n".join(output)


def parse(cron):
    if not isinstance(cron, str):
        raise TypeError("Expected a string")
    cron = cron.strip()
    parts = cron.split(" ")
    if len(parts) != 6:
        raise TypeError("Invalid cron format")
    command = parts[5]
    parsed = {}
    for idx, field in enumerate(fields):
        value = command if field == "command" else "-"
        if field == "command":
            parsed[field] = value
            continue
        for parser in parsers:
            result = parser(field, parts[idx])
            if result is not None:
                value = result
                break
        parsed[field] = value
    return formatted_output(parsed)

print(parse('*/15 0 1,15 * 1-5 /usr/bin/find'))
