from MFIS_Classes import *
from MFIS_Read_Functions import * 

'''
creates Application List object which is a wrapper for lists with a custom print method.
each application in the list has structure 
id : String (EX: 0001)
data : List<Map<String,Int>> (EX: {Age -> 35, IncomeLevel -> 82, Assets -> 38, Amount -> 8, Job -> 0, History -> 1})
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
rules_UNMODIFIED = readRulesFile()

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
fuzzySets_UNMODIFIED = readFuzzySetsFile('InputVarSets.txt')

riskFuzzySets_UNMODIFIED = readFuzzySetsFile('Risks.txt')


#applications.printApplicationList()
#rules.printRuleList()
#fuzzySets.printFuzzySetsDict()
#riskFuzzySets_UNMODIFIED.printFuzzySetsDict()



# go through each application in the list to fuzzify it
for application in applications:

  rules = rules_UNMODIFIED 
  fuzzySets = fuzzySets_UNMODIFIED 
  riskFuzzySets = riskFuzzySets_UNMODIFIED 

  '''
  STEP 1: Transform inputs into membership degree of fuzzy sets
  - take application and find how much it belongs to each set
  '''
  def transformInputs():
    #go through each Var=Value pair (EX: Age=35) in the application
    for var,value in application.data.items():
      #find the setids in the fuzzysets dict that start with var (EX: if var = age, find all entires with keys starting with age -> "Age=Young", etc)
      for setid, fuzzySet in {key: value for key, value in fuzzySets.items() if key.startswith(var)}.items():
        membership_degree = np.interp(value, fuzzySet.x, fuzzySet.y)  
        fuzzySets[setid].memDegree = membership_degree
  
  #at this point our fuzzysets dict contains the membership values for each variable in this application
  # Step 2 : Rule Evaluation
  def evaluateRules():
    for rule in rules:
      ruleConsequent = rule.consequent 
      #use min since we are evaluating using implicit ANDS
      similarityStrength = min([fuzzySets[antecedent].memDegree for antecedent in rule.antecedent])
      rule.consequentX = riskFuzzySets[ruleConsequent].x
      rule.consequentY= [y * similarityStrength for y in riskFuzzySets[ruleConsequent].y]  # Scale Y by rule strength
  
  """
  Aggregates the consequences of applicable rules into one fuzzy set.
  @param output_set_name: The specific output fuzzy set to aggregate.
  @param applicable_rules: List of rules that apply to the output set.
  """
  def aggregate(output_set_name, applicable_rules):
    aggregation = [0] * len(riskFuzzySets[output_set_name].x)
    
    for rule in applicable_rules:
        for i, y in enumerate(rule.consequentY):
            aggregation[i] = max(aggregation[i], y)
    
    return aggregation


  def defuzzify(xValues, yValues):
      """Computes the centroid for a fuzzy set."""
      if sum(yValues) == 0:
          return 0  # To handle the case where all yValues are zero
      numerator = sum(x * y for x, y in zip(xValues, yValues))
      denominator = sum(yValues)
      centroid = numerator/denominator
      return centroid

  
  transformInputs()
  evaluateRules()

  lowRiskRules = [rule for rule in rules if rule.consequent == "Risk=LowR"]
  mediumRiskRules = [rule for rule in rules if rule.consequent == "Risk=MediumR"]
  highRiskRules = [rule for rule in rules if rule.consequent == "Risk=HighR"]

  lowRiskAggregation = aggregate("Risk=LowR", lowRiskRules)
  mediumRiskAggregation = aggregate("Risk=MediumR", mediumRiskRules)
  highRiskAggregation = aggregate("Risk=HighR", highRiskRules)

  # Assuming aggregated results for each risk level:
  lowRiskCrisp = defuzzify(riskFuzzySets['Risk=LowR'].x, lowRiskAggregation)
  mediumRiskCrisp = defuzzify(riskFuzzySets['Risk=MediumR'].x, mediumRiskAggregation)
  highRiskCrisp = defuzzify(riskFuzzySets['Risk=HighR'].x, highRiskAggregation)

  highestRiskCategoryCrispValue = max(lowRiskCrisp, mediumRiskCrisp, highRiskCrisp)
  highestRiskCategory = "Error"
  if lowRiskCrisp == highestRiskCategoryCrispValue:
     highestRiskCategory = "low risk"
  elif mediumRiskCrisp == highestRiskCategoryCrispValue:
     highestRiskCategory = "medium risk"
  elif highRiskCrisp == highestRiskCategoryCrispValue:
     highestRiskCategory = "high risk"

  with open('Results.txt', 'a') as results_file:
    results_file.write(f"Application {application.appId} is {lowRiskCrisp}% low risk, {mediumRiskCrisp}% medium risk, {highRiskCrisp}% high risk. Thus we identify this application as a {highestRiskCategory} application.\n")