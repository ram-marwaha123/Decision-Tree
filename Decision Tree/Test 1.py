import math
import pandas as pd

def Entropy(p):
    value = 0
    
    if p > 0 and p < 1:
        value -= ((p * math.log(p, 2)) + ((1 - p) * math.log((1 - p), 2)))

    return value

import tree

def Remainder(A, dataset, y, positive):
    categories = dataset[A].unique()
    total = len(dataset)
    r = 0
    for c in categories:
        positives = 0
        negatives = 0
        check = dataset[A] == c
        specificData = dataset[check]

        for index, row in specificData.iterrows():
            if row[y] == positive:
                positives += 1
            else:
                negatives += 1
                
        r += ((positives + negatives)/total) * Entropy(positives / (positives + negatives))

    return r
        

def InfoGain(A, dataset, y, positive):
    p = 0
    n = 0

    for index, row in dataset.iterrows():
        if row[y] == positive:
            p += 1
        else:
            n += 1

    ig = Entropy(p/(p+n)) - Remainder(A, dataset, y, positive)
    return ig
    

dataset = pd.read_csv("TestData.csv")
#print (dataset.head())

features = ["New", "Language", "Type"] 

##for feature in features:
##    print (InfoGain(feature, dataset, "Stream", "Yes"))
##
##



class DecisionTree:
    def __init__(self):
        self.T = tree.Tree()
        pass


    def fit(self, X, y):
        self.X = X
        self.y = y
        

    def OptimiseInfoGain(self, data, features):
        Gain = [(feature, InfoGain(feature, data, self.y, "Yes")) for feature in features]

        return (max(Gain, key = lambda x: x[1]))



    def SplitData(self, data, features, node):
        attribute = features[0]
        if len(features) > 1:
            o = self.OptimiseInfoGain(data, features)
            attribute = o[0]

        
        classes = data[attribute].unique()
        
        columns = features[:]
        columns.remove(attribute)

        for c in classes:

            toSplit = data[attribute] == c
            selected_data = data[toSplit]

            
            child = tree.node({"A": attribute, "Class": c})

            p = 0
            n = 0
            
            for index, row in selected_data.iterrows():
                if  row["Stream"] == "Yes":
                    p += 1
                else:
                    n += 1

            print ("\n", attribute, c, "\n", selected_data, "\n", p, n, "\n")

            if p == 0 or n == 0:
                if n == 0:
                    leaf = tree.Leaf(1, 0)
                    child.add_node(leaf)
                else:
                    leaf = tree.Leaf(0, 1)
                    child.add_node(leaf)

                node.add_node(child)
            
            elif len (columns) == 0:
                total = p + n
                leaf = tree.Leaf(p/total, n/total)
                child.add_node(leaf)

                node.add_node(child)

            else:
                print ("enter recurse")
                self.SplitData(selected_data, columns, child)
                node.add_node(child)
                print ("exited recurse")
            print ("nodes added:", attribute, c)
        
        
        

DTree = tree.Tree()
d = DecisionTree()
d.fit(dataset, "Stream")
d.SplitData(dataset, features, DTree)

print (tree.visualise(DTree))
                              
                              

    
