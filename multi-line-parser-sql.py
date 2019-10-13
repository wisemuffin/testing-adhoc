from pprint import pprint
from collections import OrderedDict
import re

data = """ 
, "all_exclusions" = 'N'
as "order-tf"

,"order-tf"
and "fault within-tf"
and "snap date" > '2019-01-01
as "metric 1"

, "incident-tf"
as "metric2"
"""

lines = data.splitlines()
cases = ['\n'.join(lines[i:i+3]) for i in range(0, len(lines), 3)]
pattern = '(Police Response|Incident Desc|OFC|Received|Disp|Location|Event Number|ID|Priority|Case No):'
rows = []
for case in cases:
    pairs =  re.split(pattern, case)[1:]
    rows.append(OrderedDict((pairs[i*2], pairs[i*2+1]) for i in range(10)))

for i, row in enumerate(rows):
    print '============== {} =============='.format(i)
    pprint(row.items())