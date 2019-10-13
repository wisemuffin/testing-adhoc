#!/usr/bin/env python
# coding: utf-8

# # parse out SQL data for documenation
# then show the JSON in confluence:
# https://bobswift.atlassian.net/wiki/spaces/TBL/pages/131104782/JIRA+Version+List+Using+the+JSON+Table+Macro

# # Notes
# rules for input sql:
# 
# - all fields need to start with comma (except first row)
# 
# manual interventions:
# 
# - first column after select doesnt have ,

# In[1]:


import itertools
import json
inputfile = './sql-to-parse.sql'


# In[2]:


zipped = {}
n = 0
with open(inputfile, 'r') as f:

    for line in f:
#     for group, lines in itertools.groupby(f, lambda l: l.startswith(",")):
        # print 'line {} {}'.format(group, list(lines))
        zipped[n] = {'concatAbove': line.startswith(","), 'lineItem': [line]}
        n = n + 1
# print(zipped)

for key, value in zipped.items():
    print(key, '->', value)
print ('\n')


# ## Add rows together and seperate based on sql comma

# In[3]:


dict(itertools.islice(zipped.items(),3,5))


# In[4]:


dave = (12, {'concatAbove': True, 'lineItem': [', "incident-tf"\n', 'as "metric2"\n', '\n', 'from cc_dde."order_t" as "A11 Order"\n', 'inner join fld_dde."work_order_t" as "A11 Work Order" on "A11 Order"."order_key" = "A11 Work Order"."order_key"']})
"from" in dave[1]['lineItem'][3]


# In[5]:


for row in zipped:
        for rowsbelow in dict(itertools.islice(zipped.items(),row+1,len(zipped))):

            # break if row below is the start of a new field
            if zipped[rowsbelow]['concatAbove'] == True:
                break
            
            # break if row below not a field
            if 'from' in zipped[rowsbelow]['lineItem'][0]:
                break
            
            # add to the top of rows below
            zipped[row]['lineItem'] = zipped[row]['lineItem'] + zipped[rowsbelow]['lineItem']

# print(json.dumps(zipped,indent=4))
for line in zipped.items():
    print(line)


# In[6]:


zipped


# In[7]:


newDict = { key:value for (key,value) in zipped.items() if value['concatAbove'] == True}


# In[8]:


newDict


# ## remove the first comma from all lineItems

# In[9]:


for field in newDict:
    newDict[field]['lineItem'][0] = newDict[field]['lineItem'][0].replace(",","")


# ## if line has an 'as' then change that to the key

# ## if key = value then no calc
# types = calculation, or reference

# structure
# 
# [
#     {
#         columnName: x,
#         type: calculation/field,
#         calculation: x/null,
#         sourceTable: <if field>
#     },
#     {
#         columnName: x,
#         type: calculation/field,
#         calculation: x/null,
#         sourceTable: <if field>
#     }
# ]
#     
# or
# 
# {
#     columnName :{
#         type: calculation/field,
#         calculation: list of strings/null,
#         sourceTable: <if field>
#     },
#     columnName: {
#         type: calculation/field,
#         calculation: list of strings/null,
#         sourceTable: <if field>
#     }
# }

# In[10]:


documenation = {}
for field in newDict.items():
    
    # get column name from line items if as is present
    columnName = ''
    for line in field[1]['lineItem']:
        if 'as ' in line.lower():
            columnName = line[line.find('as ')+3:-1]
#             print(metricName)
            
    # if no rows have a 'as' then must just be a row
    if columnName == '':
        columnName = ''.join(field[1]['lineItem'])
    

    # if columnName = calculation then this isnt a calc! its a field
    if columnName == ''.join(field[1]['lineItem']):
        
        # split out table alias and the actual field
        if '.' in ''.join(field[1]['lineItem']):
            tableAlias, fieldTableRemoved = ''.join(field[1]['lineItem']).split('.')
            documenation[fieldTableRemoved] = {
                'type': 'field',
                'tableAlias': tableAlias
            }
        else:
            documenation[columnName] = {
                'type': 'field'
            }
    
    # else then add the calculation
    else:
        documenation[columnName] = {
            'calculation': newDict[field[0]]['lineItem'],
            'type': 'calc'
                                   }

print('\n')
for item in documenation.items():
    print(item)


# ## clean up

# ### remove filed name

# In[11]:


for key in documenation:
    if 'calculation' in documenation[key]:
        updated_calculation = []
        for line in documenation[key]['calculation']:
            if key not in line:
                updated_calculation.append(line)
        documenation[key]['calculation'] = updated_calculation

for item in documenation.items():
    print(item)
            


# ### remove new lines in calculations

# In[12]:


for key in documenation:
    if 'calculation' in documenation[key]:
        filtered_calc = filter(lambda x: x != '\n',documenation[key]['calculation'])
        documenation[key]['calculation'] = list(filtered_calc)
            


# In[13]:


for item in documenation.items():
    print(item)
            


# # recursive logic to replace fields

# In[14]:


documenation['"metric 1"']['calculation']


# In[15]:


## need to do this a few times to get rid of nested logic
for n in range(0,3):
    for key in documenation:
        if 'calculation' in documenation[key]:
            n = 0
            for calc_item in documenation[key]['calculation']:
                # if any part of the calc item is in the list of keys then replace with the key's calc
                for check_other_key in documenation.keys():
                    if check_other_key in calc_item:
                        print('bingo {} has the calc {} in {}'.format(key,check_other_key,calc_item ))
                        print('find the string in the string for {} and the replacement is {}'.format(documenation[key]['calculation'][n], documenation[check_other_key]['calculation']))
                        documenation[key]['calculation'][n] = documenation[key]['calculation'][n].replace(check_other_key,', '.join(documenation[check_other_key]['calculation'])).replace(check_other_key,' '.join(documenation[check_other_key]['calculation']))
                n = n+1
            
    


# In[16]:


documenation['"metric 1"']


# # try printing out
# need to deal with new lines and escape chars

# In[17]:


documenation


# In[18]:


for key in documenation.keys():
    print("KEY = {}".format(key))
    if 'calculation' in documenation[key]:
        print("CALCULATION = {")

        for multi_line in documenation[key]['calculation']:
            print(multi_line)
        print("}")


# In[ ]:




