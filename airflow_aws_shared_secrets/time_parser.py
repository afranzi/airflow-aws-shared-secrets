import pendulum
from pendulum import Date, DateTime, Duration, Time


def parse_timestamp(line: str) -> Date | Time | DateTime | Duration:
    timestamp_str, _ = line.split(" ", 1)
    print(f"Parsing time: {timestamp_str}")
    return pendulum.parse(timestamp_str.strip("[]"))
