from MFIS_Classes import *
from MFIS_Read_Functions import * 

'''
creates Application List object which is a wrapper for lists with a custom print method.
each application in the list has structure 
id : String (EX: 0001)
data : List<List<String,Int>> (EX: [ [Age, 35], [IncomeLevel, 82], [Assets, 38], [Amount, 8], [Job, 0], [History, 1] ])
'''
applications = readApplicationsFile()

'''
creates RuleList object which is a wrapper for lists with a custom print method.
each rule has structure 
ruleName : String -> name of the rule (str)
antecedent : List<String> -> list of setids	requried for the rule to be true
consequent : String -> just one setid that is a result of the rule
strength : float = 0 -> strength of rule, default value is 0
consequentX = []	# output fuzzySet, abscissas  ?? Dont Understand
consequentY = []	# output fuzzySet, ordinates ?? Dont Understand
'''
rules = readRulesFile()

'''
creates a fuzzySetsDict object which is a dictioary wrapper with a custom print method
each entry is of type {setID : fuzzySet Object}
setID : String set up as Var=Label (EX: 'Age=Young')
fuzzySet Object is of structure :
var : String -> variable of the fuzzy set (ex: Age)
label : String -> label of the specific fuzzy set (ex: Young)
x : List<int>	-> list of abscissas, from xmin to xmax, 1 by 1 (x values from xmin to xmax)
y : List<float>	 -> list of ordinates (float) (y values from xmin to xmax)
memDegree : float = 0  -> membership degree for the current application, default value is 0
'''
fuzzySets = readFuzzySetsFile('InputVarSets.txt')


applications.printApplicationList()
#rules.printRuleList()
fuzzySets.printFuzzySetsDict()

'''
STEP 1: Transform inputs into membership degree of fuzzy sets
- take application and find how much it belongs to each set
  ex: 
  Application 0001, Age, 35, IncomeLevel, 82, Assets, 38, Amount, 8, Job, 0, History, 1
  -> { Age Vector = [.85,.10,0], Income Vector = [...], ...} 
  in this example the age 35 is identified as 85% young, 10% middleaged, 0% old
'''
def fuzzify(application):
  membershipDegrees = {}

  for var,value in application.data:
    


#TODO: STEP 2: Rule Evaluation. Compute Antecedent and Consequent

#TODO: STEP 3: Aggregation. Unify all outputs

#TODO: STEP 4: Defuzzification.

#TODO: have code create a Results.txt file (if it doesn't already exist) and write the results of each application to a line