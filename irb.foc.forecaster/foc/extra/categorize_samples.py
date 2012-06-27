'''
Created on 8. 2. 2012.

@author: kermit
'''
import re, fileinput, sys
import os

# global
samples = {}

def output(samples, indices):
    for index in indices:
        try:
            print samples[index]
        except KeyError:
            print "no index " + str(index)
            
def eventrepl(match):
        "Return the event description string for an index string"
        value = match.group()
        try:
            desc = samples[value]
            #return bla[0]
        except KeyError:
            desc = "????"
            print "no index " + str(value)
        return desc
    
if __name__ == '__main__':
    #global samples
    with open("selection.txt") as sel, open("../description-dataset-train.txt") as data:
        # parse data
        lines = [x.rstrip() for x in data.readlines()]
        for line in lines:
            index, desc = line.split(" ")
            samples[index] = desc  
        # parse positive-negative selection
        sel_parts = sel.readline().split(" ")
        indices = [x.rstrip() for x in sel_parts[1:]]
        num = re.compile('\d+')
        if sel_parts[0]=="all":
            print "all samples: " + str(indices)
            output(samples, indices)
        elif sel_parts[0]=="file":
            filename = sel_parts[1].rstrip()
            print filename
            print os.getcwd()
            print os.listdir(".")
            filepath = os.path.join(os.getcwd(),filename)
            for i, line in enumerate(fileinput.input(filename, inplace = 1)):
                sys.stdout.write(num.sub(eventrepl, line))
        else:
            total, positive, negative = [int(x) for x in num.findall(sel_parts[0])]
            print total, positive, negative
            
            indices1 = indices[:positive]
            indices2 = indices[positive:]
            print "true positive: " + str(indices1)
            output(samples, indices1)
            print "false positive: " + str(indices2)
            output(samples, indices2)
            