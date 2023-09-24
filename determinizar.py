# input1   4;A;{D};{a,b};A,a,A;A,a,B;A,b,A;B,b,C;C,b,D
# output1  4;{A};{{AD}};{a,b};{A},a;{AB};{A},b,{A};{AB},a,{AB};{AB};b,{AC};{AC},a,{AB};{AC},b,{AD};{AD},a,{AB};{AD},b,{A}
# input2   3;A;{C};{1,2,3,&};A,1,A;A,&,B;B,2,B;B,&,C;C,3,C
# output2  3;{ABC};{{ABC},{BC},{C}};{1,2,3};{ABC},1,{ABC};{ABC},2,{BC};{ABC},3,{C};{BC},2,{BC};{BC},3,{C};{C},3,{C}
# input3   4;P;{S};{0,1};P,0,P;P,0,Q;P,1,P;Q,0,R;Q,1,R;R,0,S;S,0,S;S,1,S
# output3  8;{P};{{PQRS},{PQS},{PRS},{PS}};{0,1};{P},0,{PQ};{P},1,{P};{PQ},0,{PQR};{PQ},1,{PR};{PQR},0,{PQRS};{PQR},1,{PR};{PQRS},0,{PQRS};{PQRS},1,{PRS};{PQS},0,{PQRS};{PQS},1,{PRS};{PR},0,{PQS};{PR},1,{P};{PRS},0,{PQS};{PRS},1,{PS};{PS},0,{PQS};{PS},1,{PS}
from queue import Queue

def ReadInput():
  # afndInput = input()
  afndInput = "3;A;{C};{1,2,3,&};A,1,A;A,&,B;B,2,B;B,&,C;C,3,C"
  afndList = afndInput.split(";")
  nStates = afndList[0]
  initialState = afndList[1]
  finalStates = afndList[2]
  alphabet = afndList[3]
  transitions = afndList[4:]
  return (nStates,initialState,finalStates,alphabet,transitions)
  

def calcEpsilonClosure(transitions, initialState):
    epsilon_closure = {}

    for transition in transitions:
        state_from, symbol, state_to = transition.split(',')
        if state_from not in epsilon_closure:
            epsilon_closure[state_from] = set()
        epsilon_closure[state_from].add(state_from)

    changed = True
    while changed:
        changed = False
        for transition in transitions:
            state_from, symbol, state_to = transition.split(',')
            if symbol == '&':
                if state_from not in epsilon_closure:
                    epsilon_closure[state_from] = set()
                prev_len = len(epsilon_closure[state_from])
                epsilon_closure[state_from].update(epsilon_closure[state_to])
                if len(epsilon_closure[state_from]) > prev_len:
                    changed = True
            if transition[4] == "D":
              epsilon_closure["D"] = set()
              epsilon_closure["D"] = "D"

    
    initial_state_closure = epsilon_closure.get(initialState, set())

    epsilon_closure_sorted = {}
    for state, closure in epsilon_closure.items():
        epsilon_closure_sorted[state] = sorted(list(closure))

    return epsilon_closure_sorted, sorted(list(initial_state_closure))

def determineAutomaton(nStates ,initialState,finalStates,alphabet,transitions):
  alphabetAux = alphabet[1:-1]
  alphabetList = alphabetAux.split(",")


  allStatesClosure, initialStateClosure = calcEpsilonClosure(transitions, initialState)
  
  newStates = []
  newTrasitions = []
  newInitialState = "{" + ("".join(initialStateClosure)) + "}"
  newStates.append(newInitialState)
  newStatesQueue = Queue()
  newStatesQueue.put(newInitialState[1:-1])
  if "&" in alphabet:
    alphabetList.remove("&")          
    
  newAlphabet = "{" + ",".join(alphabetList) + "}"
  while True:
    actualState = newStatesQueue.get()
    newState = ""
    for symbol in alphabetList:
      for transition in transitions:
        if transition[0] in actualState and transition[2] == symbol:
            newState = newState + "".join(allStatesClosure[transition[4]])
          
      newState = list(newState)
      
      newState = [x for i, x in enumerate(newState) if x not in newState[:i]]
      newTrasition = "{"+actualState+"},"+symbol+",{"+"".join(newState)+"}"
      newState = "{"+"".join(newState)+"}"
      if newState not in newStates and newState != "{}":
        newStatesQueue.put(newState[1:-1])
        newStates.append(newState)
      if newTrasition not in transitions and "{}" not in newTrasition:
        newTrasitions.append(newTrasition)
      newState = ""
      
      
    if newStatesQueue.empty():
      break
  finalStatesList = finalStates[1:-1].split(",")
  newFinalStates = [] 
  for oldState in finalStatesList:
    for newS in newStates:
      if oldState in newS:
        newFinalStates.append(newS)
  newFinalStatesString = "{" + ",".join(newFinalStates) + "}"
  newNumStates = len(newStates)
  newTrasitions = sorted(newTrasitions)
  newTrasitionsString = (";".join(newTrasitions))
  # print(newStates)
  # print(newTrasitionsString)  
  # print(newStates)
  print(f"{newNumStates};{newInitialState};{newFinalStatesString};{newAlphabet};{newTrasitionsString}")
  

nStates ,initialState,finalStates,alphabet,transitions = ReadInput()
determineAutomaton(nStates ,initialState,finalStates,alphabet,transitions)


