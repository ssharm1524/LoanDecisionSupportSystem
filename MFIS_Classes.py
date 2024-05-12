#!/usr/bin/env python3
class FuzzySetsDict(dict):
    
    def printFuzzySetsDict(self):
        for elem in self:
            print("setid:     ", elem)
            self[elem].printSet()
    
class FuzzySet:
    var = ""	        # variable of the fuzzy set (ex.: Age)
    label = ""		# label of the specific fuzzy set (ex.: Young)
    x = []		# list of abscissas, from xmin to xmax, 1 by 1
    y = []		# list of ordinates (float)
    memDegree = 0       # membership degree for the current application

    def printSet(self):
        print("var:       ", self.var)
        print("label:     ", self.label)
        print("x coord:   ", self.x)
        print("y coord:   ", self.y)
        print("memDegree: ", self.memDegree)
        print()

class RuleList(list):
    def printRuleList(self):
        for elem in self:
            elem.printRule()

class Rule:
    ruleName = ""	# name of the rule (str)
    antecedent = []	# list of setids		
    consequent = ""	# just one setid
    strength = 0	# float
    consequentX = []	# output fuzzySet, abscissas
    consequentY = []	# output fuzzySet, ordinates

    def printRule(self):
        print("ruleName: ", self.ruleName)
        print("IF        ", self.antecedent)
        print("THEN      ", self.consequent)
        print("strength: ", self.strength)
        print()

class Application:
    appId = ""          # application identifier (str)
    data = {}		# dict of Var->Value

    def printApplication(self):
        print("App ID: ", self.appId)
        for var,value in self.data.items():
            print(var, " is ", value)
        print()

class ApplicationList(list):
    def printApplicationList(self):
        for app in self:
            app.printApplication()
