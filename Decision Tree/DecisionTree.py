import pandas as pd
import math
import tree

def Entropy(p):
    value = 0
    
    if p > 0 and p < 1:
        value -= ((p * math.log(p, 2)) + ((1 - p) * math.log((1 - p), 2)))

    return value


def Remainder(A, X, y, positive):
    categories = X[A].unique()
    total = len(X)
    r = 0
    for c in categories:
        positives = 0
        negatives = 0
        check = X[A] == c
        specificData = X[check]

        for index, row in specificData.iterrows():
            if y[index] == positive:
                positives += 1
            else:
                negatives += 1
                
        r += ((positives + negatives)/total) * Entropy(positives / (positives + negatives))

    return r
        

def InfoGain(A, X, y, positive):
    p = 0
    n = 0

    for index, row in X.iterrows():
        if y[index] == positive:
            p += 1
        else:
            n += 1

    ig = Entropy(p/(p+n)) - Remainder(A, dataset, y, positive)
    return ig



class DecisionTree:
    def __init__(self):
        self.T = tree.Tree()
        pass


    def fit(self, X, y):
        self.X = X
        self.y = y


    def train(self, features):
        self.SplitData(self.X, features, self.T)


    def OptimiseInfoGain(self, data, features):
        Gain = [(feature, InfoGain(feature, data, self.y, "<=50K")) for feature in features]

        return (max(Gain, key = lambda x: x[1]))


    
    def SplitData(self, data, features, node):
        attribute = features[0]
        if len(features) > 1:
            optimsed = self.OptimiseInfoGain(data, features)
            attribute = optimsed[0]

        
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
                if  self.y[index] == "<=50K":
                    p += 1
                else:
                    n += 1


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
                self.SplitData(selected_data, columns, child)
                node.add_node(child)

dataset = pd.read_csv("adult.csv")
features = ["education", "occupation", "race", "sex", "native-country"] 
#print (dataset.head())
#features = ["New", "Language", "Type"]
X = dataset[features]
#c = X["New"] == "Yes"
#print (X[c].head())

print (X.head())
y = dataset["income"]



d = DecisionTree()
d.fit(X, y)
d.train(features)
print (tree.visualise(d.T))