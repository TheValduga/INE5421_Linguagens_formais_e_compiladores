def ReadInput():
  # formato de input 3;A;C,D;a,b;AaB,BbC,CaD
  afndInput = input("digite o automato: ")
  afndList = afndInput.split(";")
  nStates = afndList[0]
  initialState = afndList[1]
  finalStates = afndList[2].split(",")
  alphabet = afndList[3].split(",")
  transitions = afndList[4].split(",")
  return (nStates,initialState,finalStates,alphabet,transitions)
  
def HasEpsilonTransitions(transitions):
  for transition in transitions:
    if "ε" in transition:
      return True
  return False

def calcEpsilonStar():
  pass

nStates, initialStates, finalStates, alphabet, transitions = ReadInput()
isEpsilon = HasEpsilonTransitions(transitions)
if isEpsilon:
  initialStateEpsilonStar, statesEpsilonStar = calcEpsilonStar()