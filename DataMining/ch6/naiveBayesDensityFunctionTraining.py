  
# 
#  Naive Bayes Classifier chapter 6
#


# _____________________________________________________________________

import math
import numpy as np

class Classifier:
    def __init__(self, bucketPrefix, testBucketNumber, dataFormat):

        """ a classifier will be built from files with the bucketPrefix
        excluding the file with textBucketNumber. dataFormat is a string that
        describes how to interpret each line of the data files. For example,
        for the iHealth data the format is:
        "attr	attr	attr	attr	class"
        """
   
        total = 0
        classes = {}
        # counts used for attributes that are not numeric
        counts = {}
        # totals used for attributes that are numereric
        # we will use these to compute the mean and sample standard deviation for
        # each attribute - class pair.
        totals = {}
        numericValues = {}
        
        
        # reading the data in from the file
        
        self.format = dataFormat.strip().split('\t')
        # 
        self.prior = {}
        self.conditional = {}
 
        # for each of the buckets numbered 1 through 10:
        for i in range(1, 11):
            # if it is not the bucket we should ignore, read in the data
            if i != testBucketNumber:
                filename = "%s-%02i" % (bucketPrefix, i)
                f = open(filename)
                lines = f.readlines()
                f.close()
                for line in lines:
                    fields = line.strip().split('\t')
                    ignore = []
                    vector = []
                    nums = []
                    for i in range(len(fields)):
                        if self.format[i] == 'num':
                            nums.append(float(fields[i]))
                        elif self.format[i] == 'attr':
                            vector.append(fields[i])                           
                        elif self.format[i] == 'comment':
                            ignore.append(fields[i])
                        elif self.format[i] == 'class':
                            category = fields[i]
                    # now process this instance
                    total += 1
                    classes.setdefault(category, 0)
                    counts.setdefault(category, {})
                    totals.setdefault(category, {})
                    numericValues.setdefault(category, {})
                    classes[category] += 1
                    # now process each non-numeric attribute of the instance
                    col = 0
                    for columnValue in vector:
                        col += 1
                        counts[category].setdefault(col, {})
                        counts[category][col].setdefault(columnValue, 0)
                        counts[category][col][columnValue] += 1
                    # process numeric attributes
                    col = 0
                    for columnValue in nums:
                        col += 1
                        totals[category].setdefault(col, 0)
                        #totals[category][col].setdefault(columnValue, 0)
                        totals[category][col] += columnValue
                        numericValues[category].setdefault(col, [])
                        numericValues[category][col].append(columnValue)
                    
        
        #
        # ok done counting. now compute probabilities
        #
        # first prior probabilities p(h)
        #
        for (category, count) in classes.items():
            self.prior[category] = count / total
        #
        # now compute conditional probabilities p(h|D)
        #
        for (category, columns) in counts.items():
              self.conditional.setdefault(category, {})
              for (col, valueCounts) in columns.items():
                  self.conditional[category].setdefault(col, {})
                  for (attrValue, count) in valueCounts.items():
                      self.conditional[category][col][attrValue] = (
                          count / classes[category])
        self.tmp =  counts 
        print "total : "+ str(totals)
        print "classes + : " +str(classes) 
        print "Numeric vals : " +str(numericValues)        
        #
        # now compute mean and sample standard deviation
        #
        self.means = {}
        self.ssd = {}
        for k in classes.keys():
            totalForKey =classes[k] 
            print totalForKey
            self.means[k] = {}
            self.ssd[k]={}
            for dic2 in totals[k].keys():
                self.means[k][dic2]=totals[k][dic2]/float(totalForKey)
                self.ssd[k][dic2]=(np.std(numericValues[k][dic2]))*math.sqrt(totalForKey)/math.sqrt(totalForKey-1)
        print self.means
        print self.ssd
        
        # ADD YOUR CODE HERE

        

 # test the code

c = Classifier("pimaSmall/pimaSmall",  1, "num	num	num	num	num	num	num	num	class")


# test means computation
assert('1' in c.means)
assert(1 in c.means['1'])
assert(c.means['1'][1] == 5.25)
assert(round(c.means['1'][2], 4) == 146.0556)
assert(round(c.means['0'][2], 4) == 111.9057)

# test standard deviation
assert('1' in c.ssd)
assert(1 in c.ssd['1'])
assert(round(c.ssd['0'][1], 4) == 2.5469)
assert(round(c.ssd['1'][8], 4) == 10.9218)
print("Means and SSD computation appears OK")
