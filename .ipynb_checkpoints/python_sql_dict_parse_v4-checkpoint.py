{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# parse out SQL data for documenation\n",
    "then show the JSON in confluence:\n",
    "https://bobswift.atlassian.net/wiki/spaces/TBL/pages/131104782/JIRA+Version+List+Using+the+JSON+Table+Macro"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Notes\n",
    "rules for input sql:\n",
    "\n",
    "- all fields need to start with comma (except first row)\n",
    "\n",
    "manual interventions:\n",
    "\n",
    "- first column after select doesnt have ,"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import itertools\n",
    "import json\n",
    "inputfile = './sql-to-parse.sql'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "0 -> {'concatAbove': False, 'lineItem': ['select\\n']}\n",
      "1 -> {'concatAbove': True, 'lineItem': [',\"A11 Order\".\"order id\"\\n']}\n",
      "2 -> {'concatAbove': True, 'lineItem': [',\"A11 Work Order\".\"work order id\"\\n']}\n",
      "3 -> {'concatAbove': False, 'lineItem': ['\\n']}\n",
      "4 -> {'concatAbove': True, 'lineItem': [', \"all_exclusions\" = \\'N\\'\\n']}\n",
      "5 -> {'concatAbove': False, 'lineItem': ['as \"order-tf\"\\n']}\n",
      "6 -> {'concatAbove': False, 'lineItem': ['\\n']}\n",
      "7 -> {'concatAbove': True, 'lineItem': [', \"inc excl\" = \\'N\\'\\n']}\n",
      "8 -> {'concatAbove': False, 'lineItem': ['and \"is inc\" = \\'Y\\'\\n']}\n",
      "9 -> {'concatAbove': False, 'lineItem': ['as \"incident-tf\"\\n']}\n",
      "10 -> {'concatAbove': False, 'lineItem': ['\\n']}\n",
      "11 -> {'concatAbove': True, 'lineItem': [',\"order-tf\"\\n']}\n",
      "12 -> {'concatAbove': False, 'lineItem': ['and \"incident-tf\"\\n']}\n",
      "13 -> {'concatAbove': False, 'lineItem': ['and \"snap date\" > \\'2019-01-01\\'\\n']}\n",
      "14 -> {'concatAbove': False, 'lineItem': ['as \"metric 1\"\\n']}\n",
      "15 -> {'concatAbove': False, 'lineItem': ['\\n']}\n",
      "16 -> {'concatAbove': True, 'lineItem': [', \"incident-tf\"\\n']}\n",
      "17 -> {'concatAbove': False, 'lineItem': ['as \"metric2\"\\n']}\n",
      "18 -> {'concatAbove': False, 'lineItem': ['\\n']}\n",
      "19 -> {'concatAbove': False, 'lineItem': ['from cc_dde.\"order_t\" as \"A11 Order\"\\n']}\n",
      "20 -> {'concatAbove': False, 'lineItem': ['inner join fld_dde.\"work_order_t\" as \"A11 Work Order\" on \"A11 Order\".\"order_key\" = \"A11 Work Order\".\"order_key\"']}\n",
      "\n",
      "\n"
     ]
    }
   ],
   "source": [
    "zipped = {}\n",
    "n = 0\n",
    "with open(inputfile, 'r') as f:\n",
    "\n",
    "    for line in f:\n",
    "#     for group, lines in itertools.groupby(f, lambda l: l.startswith(\",\")):\n",
    "        # print 'line {} {}'.format(group, list(lines))\n",
    "        zipped[n] = {'concatAbove': line.startswith(\",\"), 'lineItem': [line]}\n",
    "        n = n + 1\n",
    "# print(zipped)\n",
    "\n",
    "for key, value in zipped.items():\n",
    "    print(key, '->', value)\n",
    "print ('\\n')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Add rows together and seperate based on sql comma"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "{3: {'concatAbove': False, 'lineItem': ['\\n']},\n",
       " 4: {'concatAbove': True, 'lineItem': [', \"all_exclusions\" = \\'N\\'\\n']}}"
      ]
     },
     "execution_count": 3,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "dict(itertools.islice(zipped.items(),3,5))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "True"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "dave = (12, {'concatAbove': True, 'lineItem': [', \"incident-tf\"\\n', 'as \"metric2\"\\n', '\\n', 'from cc_dde.\"order_t\" as \"A11 Order\"\\n', 'inner join fld_dde.\"work_order_t\" as \"A11 Work Order\" on \"A11 Order\".\"order_key\" = \"A11 Work Order\".\"order_key\"']})\n",
    "\"from\" in dave[1]['lineItem'][3]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "(0, {'concatAbove': False, 'lineItem': ['select\\n']})\n",
      "(1, {'concatAbove': True, 'lineItem': [',\"A11 Order\".\"order id\"\\n']})\n",
      "(2, {'concatAbove': True, 'lineItem': [',\"A11 Work Order\".\"work order id\"\\n', '\\n']})\n",
      "(3, {'concatAbove': False, 'lineItem': ['\\n']})\n",
      "(4, {'concatAbove': True, 'lineItem': [', \"all_exclusions\" = \\'N\\'\\n', 'as \"order-tf\"\\n', '\\n']})\n",
      "(5, {'concatAbove': False, 'lineItem': ['as \"order-tf\"\\n', '\\n']})\n",
      "(6, {'concatAbove': False, 'lineItem': ['\\n']})\n",
      "(7, {'concatAbove': True, 'lineItem': [', \"inc excl\" = \\'N\\'\\n', 'and \"is inc\" = \\'Y\\'\\n', 'as \"incident-tf\"\\n', '\\n']})\n",
      "(8, {'concatAbove': False, 'lineItem': ['and \"is inc\" = \\'Y\\'\\n', 'as \"incident-tf\"\\n', '\\n']})\n",
      "(9, {'concatAbove': False, 'lineItem': ['as \"incident-tf\"\\n', '\\n']})\n",
      "(10, {'concatAbove': False, 'lineItem': ['\\n']})\n",
      "(11, {'concatAbove': True, 'lineItem': [',\"order-tf\"\\n', 'and \"incident-tf\"\\n', 'and \"snap date\" > \\'2019-01-01\\'\\n', 'as \"metric 1\"\\n', '\\n']})\n",
      "(12, {'concatAbove': False, 'lineItem': ['and \"incident-tf\"\\n', 'and \"snap date\" > \\'2019-01-01\\'\\n', 'as \"metric 1\"\\n', '\\n']})\n",
      "(13, {'concatAbove': False, 'lineItem': ['and \"snap date\" > \\'2019-01-01\\'\\n', 'as \"metric 1\"\\n', '\\n']})\n",
      "(14, {'concatAbove': False, 'lineItem': ['as \"metric 1\"\\n', '\\n']})\n",
      "(15, {'concatAbove': False, 'lineItem': ['\\n']})\n",
      "(16, {'concatAbove': True, 'lineItem': [', \"incident-tf\"\\n', 'as \"metric2\"\\n', '\\n']})\n",
      "(17, {'concatAbove': False, 'lineItem': ['as \"metric2\"\\n', '\\n']})\n",
      "(18, {'concatAbove': False, 'lineItem': ['\\n']})\n",
      "(19, {'concatAbove': False, 'lineItem': ['from cc_dde.\"order_t\" as \"A11 Order\"\\n', 'inner join fld_dde.\"work_order_t\" as \"A11 Work Order\" on \"A11 Order\".\"order_key\" = \"A11 Work Order\".\"order_key\"']})\n",
      "(20, {'concatAbove': False, 'lineItem': ['inner join fld_dde.\"work_order_t\" as \"A11 Work Order\" on \"A11 Order\".\"order_key\" = \"A11 Work Order\".\"order_key\"']})\n"
     ]
    }
   ],
   "source": [
    "for row in zipped:\n",
    "        for rowsbelow in dict(itertools.islice(zipped.items(),row+1,len(zipped))):\n",
    "\n",
    "            # break if row below is the start of a new field\n",
    "            if zipped[rowsbelow]['concatAbove'] == True:\n",
    "                break\n",
    "            \n",
    "            # break if row below not a field\n",
    "            if 'from' in zipped[rowsbelow]['lineItem'][0]:\n",
    "                break\n",
    "            \n",
    "            # add to the top of rows below\n",
    "            zipped[row]['lineItem'] = zipped[row]['lineItem'] + zipped[rowsbelow]['lineItem']\n",
    "\n",
    "# print(json.dumps(zipped,indent=4))\n",
    "for line in zipped.items():\n",
    "    print(line)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "{0: {'concatAbove': False, 'lineItem': ['select\\n']},\n",
       " 1: {'concatAbove': True, 'lineItem': [',\"A11 Order\".\"order id\"\\n']},\n",
       " 2: {'concatAbove': True,\n",
       "  'lineItem': [',\"A11 Work Order\".\"work order id\"\\n', '\\n']},\n",
       " 3: {'concatAbove': False, 'lineItem': ['\\n']},\n",
       " 4: {'concatAbove': True,\n",
       "  'lineItem': [', \"all_exclusions\" = \\'N\\'\\n', 'as \"order-tf\"\\n', '\\n']},\n",
       " 5: {'concatAbove': False, 'lineItem': ['as \"order-tf\"\\n', '\\n']},\n",
       " 6: {'concatAbove': False, 'lineItem': ['\\n']},\n",
       " 7: {'concatAbove': True,\n",
       "  'lineItem': [', \"inc excl\" = \\'N\\'\\n',\n",
       "   'and \"is inc\" = \\'Y\\'\\n',\n",
       "   'as \"incident-tf\"\\n',\n",
       "   '\\n']},\n",
       " 8: {'concatAbove': False,\n",
       "  'lineItem': ['and \"is inc\" = \\'Y\\'\\n', 'as \"incident-tf\"\\n', '\\n']},\n",
       " 9: {'concatAbove': False, 'lineItem': ['as \"incident-tf\"\\n', '\\n']},\n",
       " 10: {'concatAbove': False, 'lineItem': ['\\n']},\n",
       " 11: {'concatAbove': True,\n",
       "  'lineItem': [',\"order-tf\"\\n',\n",
       "   'and \"incident-tf\"\\n',\n",
       "   'and \"snap date\" > \\'2019-01-01\\'\\n',\n",
       "   'as \"metric 1\"\\n',\n",
       "   '\\n']},\n",
       " 12: {'concatAbove': False,\n",
       "  'lineItem': ['and \"incident-tf\"\\n',\n",
       "   'and \"snap date\" > \\'2019-01-01\\'\\n',\n",
       "   'as \"metric 1\"\\n',\n",
       "   '\\n']},\n",
       " 13: {'concatAbove': False,\n",
       "  'lineItem': ['and \"snap date\" > \\'2019-01-01\\'\\n', 'as \"metric 1\"\\n', '\\n']},\n",
       " 14: {'concatAbove': False, 'lineItem': ['as \"metric 1\"\\n', '\\n']},\n",
       " 15: {'concatAbove': False, 'lineItem': ['\\n']},\n",
       " 16: {'concatAbove': True,\n",
       "  'lineItem': [', \"incident-tf\"\\n', 'as \"metric2\"\\n', '\\n']},\n",
       " 17: {'concatAbove': False, 'lineItem': ['as \"metric2\"\\n', '\\n']},\n",
       " 18: {'concatAbove': False, 'lineItem': ['\\n']},\n",
       " 19: {'concatAbove': False,\n",
       "  'lineItem': ['from cc_dde.\"order_t\" as \"A11 Order\"\\n',\n",
       "   'inner join fld_dde.\"work_order_t\" as \"A11 Work Order\" on \"A11 Order\".\"order_key\" = \"A11 Work Order\".\"order_key\"']},\n",
       " 20: {'concatAbove': False,\n",
       "  'lineItem': ['inner join fld_dde.\"work_order_t\" as \"A11 Work Order\" on \"A11 Order\".\"order_key\" = \"A11 Work Order\".\"order_key\"']}}"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "zipped"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "newDict = { key:value for (key,value) in zipped.items() if value['concatAbove'] == True}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "{1: {'concatAbove': True, 'lineItem': [',\"A11 Order\".\"order id\"\\n']},\n",
       " 2: {'concatAbove': True,\n",
       "  'lineItem': [',\"A11 Work Order\".\"work order id\"\\n', '\\n']},\n",
       " 4: {'concatAbove': True,\n",
       "  'lineItem': [', \"all_exclusions\" = \\'N\\'\\n', 'as \"order-tf\"\\n', '\\n']},\n",
       " 7: {'concatAbove': True,\n",
       "  'lineItem': [', \"inc excl\" = \\'N\\'\\n',\n",
       "   'and \"is inc\" = \\'Y\\'\\n',\n",
       "   'as \"incident-tf\"\\n',\n",
       "   '\\n']},\n",
       " 11: {'concatAbove': True,\n",
       "  'lineItem': [',\"order-tf\"\\n',\n",
       "   'and \"incident-tf\"\\n',\n",
       "   'and \"snap date\" > \\'2019-01-01\\'\\n',\n",
       "   'as \"metric 1\"\\n',\n",
       "   '\\n']},\n",
       " 16: {'concatAbove': True,\n",
       "  'lineItem': [', \"incident-tf\"\\n', 'as \"metric2\"\\n', '\\n']}}"
      ]
     },
     "execution_count": 8,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "newDict"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## remove the first comma from all lineItems"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "for field in newDict:\n",
    "    newDict[field]['lineItem'][0] = newDict[field]['lineItem'][0].replace(\",\",\"\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## if line has an 'as' then change that to the key"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## if key = value then no calc\n",
    "types = calculation, or reference"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "structure\n",
    "\n",
    "[\n",
    "    {\n",
    "        columnName: x,\n",
    "        type: calculation/field,\n",
    "        calculation: x/null,\n",
    "        sourceTable: <if field>\n",
    "    },\n",
    "    {\n",
    "        columnName: x,\n",
    "        type: calculation/field,\n",
    "        calculation: x/null,\n",
    "        sourceTable: <if field>\n",
    "    }\n",
    "]\n",
    "    \n",
    "or\n",
    "\n",
    "{\n",
    "    columnName :{\n",
    "        type: calculation/field,\n",
    "        calculation: list of strings/null,\n",
    "        sourceTable: <if field>\n",
    "    },\n",
    "    columnName: {\n",
    "        type: calculation/field,\n",
    "        calculation: list of strings/null,\n",
    "        sourceTable: <if field>\n",
    "    }\n",
    "}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n",
      "\n",
      "('\"order id\"\\n', {'type': 'field', 'tableAlias': '\"A11 Order\"'})\n",
      "('\"work order id\"\\n\\n', {'type': 'field', 'tableAlias': '\"A11 Work Order\"'})\n",
      "('\"order-tf\"', {'calculation': [' \"all_exclusions\" = \\'N\\'\\n', 'as \"order-tf\"\\n', '\\n'], 'type': 'calc'})\n",
      "('\"incident-tf\"', {'calculation': [' \"inc excl\" = \\'N\\'\\n', 'and \"is inc\" = \\'Y\\'\\n', 'as \"incident-tf\"\\n', '\\n'], 'type': 'calc'})\n",
      "('\"metric 1\"', {'calculation': ['\"order-tf\"\\n', 'and \"incident-tf\"\\n', 'and \"snap date\" > \\'2019-01-01\\'\\n', 'as \"metric 1\"\\n', '\\n'], 'type': 'calc'})\n",
      "('\"metric2\"', {'calculation': [' \"incident-tf\"\\n', 'as \"metric2\"\\n', '\\n'], 'type': 'calc'})\n"
     ]
    }
   ],
   "source": [
    "documenation = {}\n",
    "for field in newDict.items():\n",
    "    \n",
    "    # get column name from line items if as is present\n",
    "    columnName = ''\n",
    "    for line in field[1]['lineItem']:\n",
    "        if 'as ' in line.lower():\n",
    "            columnName = line[line.find('as ')+3:-1]\n",
    "#             print(metricName)\n",
    "            \n",
    "    # if no rows have a 'as' then must just be a row\n",
    "    if columnName == '':\n",
    "        columnName = ''.join(field[1]['lineItem'])\n",
    "    \n",
    "\n",
    "    # if columnName = calculation then this isnt a calc! its a field\n",
    "    if columnName == ''.join(field[1]['lineItem']):\n",
    "        \n",
    "        # split out table alias and the actual field\n",
    "        if '.' in ''.join(field[1]['lineItem']):\n",
    "            tableAlias, fieldTableRemoved = ''.join(field[1]['lineItem']).split('.')\n",
    "            documenation[fieldTableRemoved] = {\n",
    "                'type': 'field',\n",
    "                'tableAlias': tableAlias\n",
    "            }\n",
    "        else:\n",
    "            documenation[columnName] = {\n",
    "                'type': 'field'\n",
    "            }\n",
    "    \n",
    "    # else then add the calculation\n",
    "    else:\n",
    "        documenation[columnName] = {\n",
    "            'calculation': newDict[field[0]]['lineItem'],\n",
    "            'type': 'calc'\n",
    "                                   }\n",
    "\n",
    "print('\\n')\n",
    "for item in documenation.items():\n",
    "    print(item)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## clean up"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### remove filed name"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "('\"order id\"\\n', {'type': 'field', 'tableAlias': '\"A11 Order\"'})\n",
      "('\"work order id\"\\n\\n', {'type': 'field', 'tableAlias': '\"A11 Work Order\"'})\n",
      "('\"order-tf\"', {'calculation': [' \"all_exclusions\" = \\'N\\'\\n', '\\n'], 'type': 'calc'})\n",
      "('\"incident-tf\"', {'calculation': [' \"inc excl\" = \\'N\\'\\n', 'and \"is inc\" = \\'Y\\'\\n', '\\n'], 'type': 'calc'})\n",
      "('\"metric 1\"', {'calculation': ['\"order-tf\"\\n', 'and \"incident-tf\"\\n', 'and \"snap date\" > \\'2019-01-01\\'\\n', '\\n'], 'type': 'calc'})\n",
      "('\"metric2\"', {'calculation': [' \"incident-tf\"\\n', '\\n'], 'type': 'calc'})\n"
     ]
    }
   ],
   "source": [
    "for key in documenation:\n",
    "    if 'calculation' in documenation[key]:\n",
    "        updated_calculation = []\n",
    "        for line in documenation[key]['calculation']:\n",
    "            if key not in line:\n",
    "                updated_calculation.append(line)\n",
    "        documenation[key]['calculation'] = updated_calculation\n",
    "\n",
    "for item in documenation.items():\n",
    "    print(item)\n",
    "            "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### remove new lines in calculations"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "for key in documenation:\n",
    "    if 'calculation' in documenation[key]:\n",
    "        filtered_calc = filter(lambda x: x != '\\n',documenation[key]['calculation'])\n",
    "        documenation[key]['calculation'] = list(filtered_calc)\n",
    "            "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "('\"order id\"\\n', {'type': 'field', 'tableAlias': '\"A11 Order\"'})\n",
      "('\"work order id\"\\n\\n', {'type': 'field', 'tableAlias': '\"A11 Work Order\"'})\n",
      "('\"order-tf\"', {'calculation': [' \"all_exclusions\" = \\'N\\'\\n'], 'type': 'calc'})\n",
      "('\"incident-tf\"', {'calculation': [' \"inc excl\" = \\'N\\'\\n', 'and \"is inc\" = \\'Y\\'\\n'], 'type': 'calc'})\n",
      "('\"metric 1\"', {'calculation': ['\"order-tf\"\\n', 'and \"incident-tf\"\\n', 'and \"snap date\" > \\'2019-01-01\\'\\n'], 'type': 'calc'})\n",
      "('\"metric2\"', {'calculation': [' \"incident-tf\"\\n'], 'type': 'calc'})\n"
     ]
    }
   ],
   "source": [
    "for item in documenation.items():\n",
    "    print(item)\n",
    "            "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# recursive logic to replace fields"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "['\"order-tf\"\\n', 'and \"incident-tf\"\\n', 'and \"snap date\" > \\'2019-01-01\\'\\n']"
      ]
     },
     "execution_count": 14,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "documenation['\"metric 1\"']['calculation']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "bingo \"metric 1\" has the calc \"order-tf\" in \"order-tf\"\n",
      "\n",
      "find the string in the string for \"order-tf\"\n",
      " and the replacement is [' \"all_exclusions\" = \\'N\\'\\n']\n",
      "bingo \"metric 1\" has the calc \"incident-tf\" in and \"incident-tf\"\n",
      "\n",
      "find the string in the string for and \"incident-tf\"\n",
      " and the replacement is [' \"inc excl\" = \\'N\\'\\n', 'and \"is inc\" = \\'Y\\'\\n']\n",
      "bingo \"metric2\" has the calc \"incident-tf\" in  \"incident-tf\"\n",
      "\n",
      "find the string in the string for  \"incident-tf\"\n",
      " and the replacement is [' \"inc excl\" = \\'N\\'\\n', 'and \"is inc\" = \\'Y\\'\\n']\n"
     ]
    }
   ],
   "source": [
    "## need to do this a few times to get rid of nested logic\n",
    "for n in range(0,3):\n",
    "    for key in documenation:\n",
    "        if 'calculation' in documenation[key]:\n",
    "            n = 0\n",
    "            for calc_item in documenation[key]['calculation']:\n",
    "                # if any part of the calc item is in the list of keys then replace with the key's calc\n",
    "                for check_other_key in documenation.keys():\n",
    "                    if check_other_key in calc_item:\n",
    "                        print('bingo {} has the calc {} in {}'.format(key,check_other_key,calc_item ))\n",
    "                        print('find the string in the string for {} and the replacement is {}'.format(documenation[key]['calculation'][n], documenation[check_other_key]['calculation']))\n",
    "                        documenation[key]['calculation'][n] = documenation[key]['calculation'][n].replace(check_other_key,', '.join(documenation[check_other_key]['calculation'])).replace(check_other_key,' '.join(documenation[check_other_key]['calculation']))\n",
    "                n = n+1\n",
    "            \n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "{'calculation': [' \"all_exclusions\" = \\'N\\'\\n\\n',\n",
       "  'and  \"inc excl\" = \\'N\\'\\n, and \"is inc\" = \\'Y\\'\\n\\n',\n",
       "  'and \"snap date\" > \\'2019-01-01\\'\\n'],\n",
       " 'type': 'calc'}"
      ]
     },
     "execution_count": 16,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "documenation['\"metric 1\"']"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# try printing out\n",
    "need to deal with new lines and escape chars"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "{'\"order id\"\\n': {'type': 'field', 'tableAlias': '\"A11 Order\"'},\n",
       " '\"work order id\"\\n\\n': {'type': 'field', 'tableAlias': '\"A11 Work Order\"'},\n",
       " '\"order-tf\"': {'calculation': [' \"all_exclusions\" = \\'N\\'\\n'],\n",
       "  'type': 'calc'},\n",
       " '\"incident-tf\"': {'calculation': [' \"inc excl\" = \\'N\\'\\n',\n",
       "   'and \"is inc\" = \\'Y\\'\\n'],\n",
       "  'type': 'calc'},\n",
       " '\"metric 1\"': {'calculation': [' \"all_exclusions\" = \\'N\\'\\n\\n',\n",
       "   'and  \"inc excl\" = \\'N\\'\\n, and \"is inc\" = \\'Y\\'\\n\\n',\n",
       "   'and \"snap date\" > \\'2019-01-01\\'\\n'],\n",
       "  'type': 'calc'},\n",
       " '\"metric2\"': {'calculation': ['  \"inc excl\" = \\'N\\'\\n, and \"is inc\" = \\'Y\\'\\n\\n'],\n",
       "  'type': 'calc'}}"
      ]
     },
     "execution_count": 17,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "documenation"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "KEY = \"order id\"\n",
      "\n",
      "KEY = \"work order id\"\n",
      "\n",
      "\n",
      "KEY = \"order-tf\"\n",
      "CALCULATION = {\n",
      " \"all_exclusions\" = 'N'\n",
      "\n",
      "}\n",
      "KEY = \"incident-tf\"\n",
      "CALCULATION = {\n",
      " \"inc excl\" = 'N'\n",
      "\n",
      "and \"is inc\" = 'Y'\n",
      "\n",
      "}\n",
      "KEY = \"metric 1\"\n",
      "CALCULATION = {\n",
      " \"all_exclusions\" = 'N'\n",
      "\n",
      "\n",
      "and  \"inc excl\" = 'N'\n",
      ", and \"is inc\" = 'Y'\n",
      "\n",
      "\n",
      "and \"snap date\" > '2019-01-01'\n",
      "\n",
      "}\n",
      "KEY = \"metric2\"\n",
      "CALCULATION = {\n",
      "  \"inc excl\" = 'N'\n",
      ", and \"is inc\" = 'Y'\n",
      "\n",
      "\n",
      "}\n"
     ]
    }
   ],
   "source": [
    "for key in documenation.keys():\n",
    "    print(\"KEY = {}\".format(key))\n",
    "    if 'calculation' in documenation[key]:\n",
    "        print(\"CALCULATION = {\")\n",
    "\n",
    "        for multi_line in documenation[key]['calculation']:\n",
    "            print(multi_line)\n",
    "        print(\"}\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python-and-Spark-for-Big-Data-master",
   "language": "python",
   "name": "python-and-spark-for-big-data-master"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.4"
  },
  "toc": {
   "base_numbering": 1,
   "nav_menu": {},
   "number_sections": true,
   "sideBar": true,
   "skip_h1_title": false,
   "title_cell": "Table of Contents",
   "title_sidebar": "Contents",
   "toc_cell": false,
   "toc_position": {},
   "toc_section_display": true,
   "toc_window_display": false
  },
  "varInspector": {
   "cols": {
    "lenName": 16,
    "lenType": 16,
    "lenVar": 40
   },
   "kernels_config": {
    "python": {
     "delete_cmd_postfix": "",
     "delete_cmd_prefix": "del ",
     "library": "var_list.py",
     "varRefreshCmd": "print(var_dic_list())"
    },
    "r": {
     "delete_cmd_postfix": ") ",
     "delete_cmd_prefix": "rm(",
     "library": "var_list.r",
     "varRefreshCmd": "cat(var_dic_list()) "
    }
   },
   "types_to_exclude": [
    "module",
    "function",
    "builtin_function_or_method",
    "instance",
    "_Feature"
   ],
   "window_display": false
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
