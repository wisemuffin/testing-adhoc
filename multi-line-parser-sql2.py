import itertools
import json
inputfile = './sql-to-parse.sql'

# with open(inputfile, 'r') as infile:
#     for line in infile:
#         if line.startswith(","):
#             print line, # comma on the end prevents the double spacing from printing a file line
#             for line in infile:
#                 print line,
#                 if line.startswith(","):
#                     break # stop this inner for loop; outer loop picks up on the next line

# should_print = False
# with open(inputfile, 'r') as infile:
#     for line in infile:
#         if line.startswith(","):
#             # should_print becomes True if was False and becomes False if was True
#             should_print = not should_print
#         if should_print:
#             print(line)

zipped = {}
n = 0
with open(inputfile, 'r') as f:

    for group, lines in itertools.groupby(f, lambda l: l.startswith(",")):
        # print 'line {} {}'.format(group, list(lines))
        zipped[n] = {'concatAbove': group, 'lineItem': list(lines)}
        n = n + 1
# print(zipped)

for key, value in zipped.items():
    print(key, '->', value)
print '\n'

print 'length of zipped = {}'.format(len(zipped))
print '\n'

concatLine = dict(zipped)
print type(concatLine)
for row in concatLine:

    # print zipped[row]['concatAbove'] == False

    # if row starts with a comma (,)
    if concatLine[row]['concatAbove'] == True:

        for rowsbelow in concatLine[row:-1]:
            if rowsbelow['concatAbove'] == True:
                break
            concatLine[row]['lineItem'].append(
                concatLine[rowsbelow]['lineItem'])

        # print zipped[row]

        # concatLine[row] = dict(zipped[row])

        # check for rows below without comma (,) and add them together

        # if concatLine[row+1]['concatAbove'] == False:

        #     x = 1

        #     while concatLine[row+x]['concatAbove'] == False and concatLine[row+x].key() < len(concatLine)+1:
        #         # print zipped[row+x]
        #         concatLine[row]['lineItem'].append(
        #             concatLine[row+x]['lineItem'])
        #         x = x + 1
        #         print 'x is {}'.format(x)

            # concatLine[row]['lineItem'].append(zipped[row+x]['lineItem'])

            # res_list = [y for x in [test_list1, test_list2] for y in x]

            # concatLine[row]['lineItem'] = [y for z in [
            #     concatLine[row]['lineItem'], zipped[row+x]['lineItem']] for y in z]

for item in concatLine:
    print concatLine[item]
