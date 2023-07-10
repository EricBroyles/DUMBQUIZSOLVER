import re
text = """The 3-day delivery process for US Treasury futures includes:
( - ) Intention Day, Notice Day, and Delivery Day
O Decision Day, Interest Day and Delivery Day
- ) Yield Day, Notice Day and Trade Day
- ) Intention Day, Yield Day and Decision Day
True or false: CME U.S. Treasury notes and bond futures may be settled through
physical delivery.
© True
©) False
True or false: An important and defining feature of US Treasury futures is that
short position may deliver security for contract on any business day of the
expiring quarterly contract month.
© Tue
© False
How can a long Treasury futures holder avoid unexpected position delivery?
( - ) By rolling a soon-to-expire long position into the next contract month
- ) Alllong positions are subject to unexpected delivery so long as the position is open
_) By keeping a soon-to-expire long position from rolling into the next contract month
o hello my name is
0 no my name is is
A yo no it isint
I have 0 dollars
obligations
"""

lines = text.split("\n")

for line in lines:

    # pattern = r"[^Aa0-9]+[A-Za-z](?![A-Za-z0-9])"TRASH
    pattern = r"^[^A-Za-z0-9]+" #matches any number of special characters at the begining
    pattern2 = r"^[oO0]\b"
    match = re.search(pattern, line)
    match2 = re.search(pattern2, line)

    if match:
        print(match.group())
    elif match2:
        print(match2.group())
    else:
        print("No match found.")

