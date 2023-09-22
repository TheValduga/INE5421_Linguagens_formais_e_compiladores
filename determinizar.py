# input1   4;A;{D};{a,b};A,a,A;A,a,B;A,b,A;B,b,C;C,b,D
# output1  4;{A};{{AD}};{a,b};{A},a;{AB};{A},b,{A};{AB},a,{AB};{AB};b,{AC};{AC},a,{AB};{AC},b,{AD};{AD},a,{AB};{AD},b,{A}
# input2   3;A;{C};{1,2,3,&};A,1,A;A,&,B;B,2,B;B,&,C;C,3,C
# output2  3;{ABC};{{ABC},{BC},{C}};{1,2,3};{ABC},1,{ABC};{ABC},2,{BC};{ABC},3,{C};{BC},2,{BC};{BC},3,{C};{C},3,{C}
# input3   4;P;{S};{0,1};P,0,P;P,0,Q;P,1,P;Q,0,R;Q,1,R;R,0,S;S,0,S;S,1,S
# output3  8;{P};{{PQRS},{PQS},{PRS},{PS}};{0,1};{P},0,{PQ};{P},1,{P};{PQ},0,{PQR};{PQ},1,{PR};{PQR},0,{PQRS};{PQR},1,{PR};{PQRS},0,{PQRS};{PQRS},1,{PRS};{PQS},0,{PQRS};{PQS},1,{PRS};{PR},0,{PQS};{PR},1,{P};{PRS},0,{PQS};{PRS},1,{PS};{PS},0,{PQS};{PS},1,{PS}

def ReadInput():
  afndInput = input()
  afndList = afndInput.split(";")
  print(afndList)
  nStates = afndList[0]
  initialState = afndList[1]
  finalStates = afndList[2]
  alphabet = afndList[3]
  transitions = afndList[4:]
  return (nStates,initialState,finalStates,alphabet,transitions)
  
def HasEpsilonTransitions(transitions):
  for transition in transitions:
    if "&" in transition:
      return True
  return False

def calcEpsilonStar(transitions):
  pass

nStates, initialStates, finalStates, alphabet, transitions = ReadInput()
isEpsilon = HasEpsilonTransitions(transitions)
if isEpsilon:
  initialStateEpsilonStar, statesEpsilonStar = calcEpsilonStar()
  
  def calcEpsilonStar(transitions):
    epsilon_closure = {}  # Dictionary to store epsilon closures for each state

    # Initialize epsilon closure with the states themselves
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
                # Add epsilon closure of state_to to state_from's epsilon closure
                if state_from not in epsilon_closure:
                    epsilon_closure[state_from] = set()
                prev_len = len(epsilon_closure[state_from])
                epsilon_closure[state_from].update(epsilon_closure[state_to])
                if len(epsilon_closure[state_from]) > prev_len:
                    changed = True

    return epsilon_closure

# Example input
input_str = "4;A;{D};{a,b};A,a,A;A,a,B;A,b,A;B,b,C;C,b,D"

# Parse the input and extract transitions
input_parts = input_str.split(';')
transitions = input_parts[4:]

# Calculate epsilon closure
epsilon_closure = calcEpsilonStar(transitions)

# Print epsilon closure for each state
for state, closure in epsilon_closure.items():
    print(f"Epsilon Closure of State {state}: {', '.join(closure)}")
