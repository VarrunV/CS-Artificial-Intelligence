#Game of knights, spies, knaves

#Three statements from A, B, C
#First instances, ind
icate what each person says
#Next instance to figure who is lying and who is telling the truth




from logic2 import ATOM, AND, OR, NOT
import DPLL2

######### Cardinality constraints #########

def atLeast1(fmas):
  return OR(fmas)

def allpairs(lst): # Helper function for atMost1
  return [ (lst[i],lst[j]) for i in range(0,len(lst)) for j in range(i+1,len(lst)) ]

def atMost1(fmas):
  return AND([NOT(AND([f1,f2])) for (f1,f2) in allpairs(fmas)])

def exactly1(fmas):
  return AND([atMost1(fmas), atLeast1(fmas)])

people = ("A","B","C")
roles = ("Knight", "Knave", "Spy")
def isa(p,r):
    "Define an atom stating '<person> is a <role>'"
    return ATOM("{0} is a {1}".format(p,r))
def claim(p):
    "Define an atom stating that a person speaks the truth."
    return ATOM("{0}'s statement holds".format(p))

# The code template below assumes that each person gives
# exactly one statement

statement = {}

# Test 1
#statement["A"] = isa("A","Knight") # I am a knight
#statement["B"] = claim("A") # That is correct
#statement["C"] = isa("C","Spy") # I am a spy

# Test 2
statement["A"] = isa("A","Spy") # I am the spy.
statement["B"] = claim("A") # That is correct.
statement["C"] = NOT(isa("C","Spy")) # I am not a spy.

# Build formula from given statements
def makeFormulas(statement):
  constraints = []
  # Roles are mutually exclusive
  constraints.append(AND([exactly1([isa(p,r) for r in roles]) for p in people]))
  # And only one role per person
  constraints.append(AND([exactly1([isa(p,r) for p in people]) for r in roles]))
  for p in people:
    # A person is either speaking the truth and is a knight or a spy. Their statement is true.
    # AND(OR([claim(p)],[isa(p, "Spy"), isa(p,"Knight")]))
    # AND([claim(p), OR([isa(p, "Spy"), isa(p, "Knight")])])
    # Or, the person is lying and is a knave or a spy. Their statement is false.
    # AND([NOT(claim(p)), OR([isa(p,"Spy"), isa(p, "Knave")]))
    constraints.append(
      OR(
        [
          AND(
            [
              claim(p), OR([isa(p, "Spy"), isa(p, "Knight")])
            ]
          ),
          AND(
            [
              NOT(claim(p)), OR([isa(p, "Spy"), isa(p, "Knave")])
            ]
          )
        ]
      )
    )

  return AND(constraints)

#for c in constraints:
#  print(c)

sol = DPLL2.SAT(makeFormulas(statement))

# Show True atoms in valuation
for p in people:
  def truthlies(t):
    if t:
      return "tells the truth"
    else:
      return "lies"
  for r in roles:
    if sol[str(isa(p,r))]:
      print("{0} and {1}".format(isa(p,r),truthlies(sol[str(claim(p))])))
