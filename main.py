import random
import copy
import bisect 
class Units():
  def __init__(self, num, dice):
    self.num = int(num)
    self.lessThan = int(dice)
  def fire(self):
    hits = 0
    for n in range(self.num):
      roll = random.randint(1,6)
      if roll<=self.lessThan:
        hits +=1
    return hits
  def Confirm(self):
    print("group of",self.num,"units that hit by",self.lessThan,"or less")
    ok = input("is this correct? y/n  ")
    if ok == "y":
      return(True)
    else:
      print("Canceled")
      return(False)
  def printStats(self):
      print("group of",self.num,"units that hit by",self.lessThan,"or less")
  def hit(self,hits):
    self.num -= hits
    if self.num > 0:
      return -1
    elif self.num == 0:
      return 0
    else:
      return self.num*-1
def MakeUnits(usrInput):
  tokens = usrInput.split()
  units = Units(tokens[0],tokens[1])
  return units

  
print("Battle win percentage calculator")
print("Enter attacking units:")
attackers = []
usrInput = input("enter a group of units in form: number_of_units roll_or_less\n") # q to quit
while usrInput != "q":
  units = MakeUnits(usrInput)
  if units.Confirm():
    attackers.append(units)
  usrInput = input("\nenter another group of units in form: number_of_units roll_or_less\n")
print("\nAttacker stats:")
for units in attackers:
  units.printStats()

print("\n\nEnter defending units:")
defenders = []
usrInput = input("enter a group of units in form: number_of_units roll_or_less\n") # q to quit
while usrInput != "q":
  units = MakeUnits(usrInput)
  if units.Confirm():
    defenders.append(units)
  usrInput = input("\nenter another group of units in form: number_of_units roll_or_less\n")
print("\nDefender stats:")
for units in defenders:
  units.printStats()

tests = int(input("how many simulations should be run of this battle?  "))
savedAttackers = copy.deepcopy(attackers)
savedDefenders = copy.deepcopy(defenders)
AtkWins = 0
DefWins = 0
avgRemaining = 0
remainList = []
for n in range(tests):
  attackers = copy.deepcopy(savedAttackers)
  defenders = copy.deepcopy(savedDefenders)
  turn = 0
  done = False
  while not done:
    turn +=1
    DefCasualties = 0
    AtkCasualties = 0

    for units in attackers:
      DefCasualties += units.fire()

    for units in defenders:
      AtkCasualties += units.fire()
    while DefCasualties > 0:
      DefCasualties = defenders[0].hit(DefCasualties)
      if DefCasualties >= 0:
        del(defenders[0])
      if len(defenders) == 0:
        done = True
  
        break
  
    while AtkCasualties > 0:
      AtkCasualties = attackers[0].hit(AtkCasualties)
      if AtkCasualties >= 0:
        del(attackers[0])
      if len(attackers) == 0:
        done = True
        break

  if len(attackers)>0:
    remaining = 0
    for units in attackers:
      remaining += units.num
    avgRemaining += remaining
    bisect.insort(remainList,remaining)
    AtkWins +=1
    done = True
  else:
    remaining = 0
    for units in defenders:
      remaining += units.num
    avgRemaining -= remaining
    bisect.insort(remainList,-remaining)
    DefWins+=1
    done = True
avgRemaining /=tests
defenderPercentage = (DefWins/(DefWins+AtkWins))*100
print("\n\n\nThe defender has a",defenderPercentage,"% win probability")
AttackerPercentage = (AtkWins/(DefWins+AtkWins))*100
print("The attacker has a",AttackerPercentage,"% win probability")
if avgRemaining>0:
  print("The attacker will probably keep",(avgRemaining),"units")
else:
  print("The defender will probably keep",-(avgRemaining),"units")
AtkBest = remainList[-1]
DefBest = remainList[0]
difference = AtkBest - DefBest

if difference>20:

  step = difference/20
else:

  step = 1
under = DefBest+step
index = 0
print(-DefBest,":",end="")
while under<AtkBest:
  if under < remainList[index]:
    print("\n",abs(int(under)),":",end="")
    under+=step
  else:
    print("#",end = '')
    index+=1

  