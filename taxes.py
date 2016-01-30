def CV(label):
    return cell_list[label].value

exec(open("cells.py").read())

def add_a_form(name):
    global cell_list
    cell_list =dict(list(cell_list.items()) + list(eval(name).items()))


exec(open("forms/f1040.py").read())
add_a_form('f1040')

exec(open("forms/schedule_a.py").read())
add_a_form('schedule_a')

def setup_inform():
    f = open("inform.py", "w")
    for i in cell_list.values():
        if (i.flag=='u'):
            f.write(
"""
#%s
%s = 0
""" % (i.name, i.calc))
    f.close

def print_a_form(name, inlist):
    print(">>>>>>>>>> %s <<<<<<<<<" %(name,))
    out=list()
    for i in inlist.keys():
    	out.append((cell_list[i].line, cell_list[i].name, cell_list[i].value))
    out.sort()
    max_len = 0
    for i in out:
    	max_len = max(max_len, len(i[1]))
    for i in out:
    	print("%4g | %*s | %g" %( i[0], max_len, i[1], i[2]))

def print_the_tree(starting_cell, level=0):
    print("%s├ %s=%g" % ("│   "*level, starting_cell, CV(starting_cell)))
    parents = cell_list[starting_cell].parents
    if (parents != None):
        print("%s├───┐" % ("│   "*level))
        for i in parents:
            print_the_tree(i, level+1)

# The main routine: build interview and inform, calculate taxes, print

status="no interview yet"

import pathlib, sys
from shutil import copyfile
if (not pathlib.Path("interview.py").exists()):
    copyfile("forms/interview_template.py", "interview.py")
    print("Have generated interview.py. Please fill it in and rerun this script.")
    sys.exit(1)

exec(open("interview.py").read())
if (status=="no interview yet"):
    print("Please follow the steps in interview.py and rerun this script.")
    sys.exit(1)

if (not pathlib.Path("inform.py").exists()):
    setup_inform()
    print("Have generated inform.py. Please fill it in and rerun this script.")
    sys.exit(1)

from inform import *

print(cell_list['refund'].name, cell_list['refund'].compute())
print(cell_list['tax_owed'].name, cell_list['tax_owed'].compute())
print_a_form("Form 1040", f1040)

print("\n")
print_the_tree('refund')
