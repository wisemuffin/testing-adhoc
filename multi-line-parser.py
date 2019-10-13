from pprint import pprint
from collections import OrderedDict
import re

data = """Police Response: 11/6/2012 1:34:06 AM   Incident Desc: Traffic Stop OFC:    Received: 11/6/2012 1:34:06 AM
Disp: PCHK  Location: CLEAR LAKE RD&GREEN HILL RD
Event Number: LLS121106060941   ID: 60941   Priority: 6 Case No:
Police Response:    Incident Desc: Theft    OFC:    Received: 11/6/2012 1:43:35 AM
Disp: CSR   Location: SCH BLACHLY
Event Number: LLS121106060943   ID: 60943   Priority: 4 Case No:
Police Response: 11/6/2012 1:47:47 AM   Incident Desc: Suspicious Vehicle(s)    OFC:        Received: 11/6/2012 1:47:47 AM
Disp: FI    Location: KIRK RD&CLEAR LAKE RD
Event Number: LLS121106060944   ID: 60944   Priority: 6 Case No: """

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