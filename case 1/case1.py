#import pyhop
from pyhop import hop

# Primitive tasks
# goto from location x to location y
def goto(state,r, x, y):
    if state.loc[r] == x:
        state.loc[r] = y
        return state
    else:
        return False

#Compound tasks
# x:object y:location
def pick(state,r,o,y):
    if(state.loc[o] == y and state.gripper == True and state.loc[r] == y):
        state.gripper = False
        state.loc[o] = r
        return state
    else:
        return False


def place(state,r,o,x):
    if(state.loc[o] == r and state.gripper == False and state.loc[r]== x and state.cupDoorisopen == True):
        state.gripper = True
        state.loc[o] = x
        return state
    else:
        return False
        # state.gripper = True
        # state.loc[o] = tray
        # return state

def open(state,r,x):
    if(state.gripper == True and state.cupDoorisopen == False and state.loc[r] == x):
        state.cupDoorisopen = True
        return state
#initial state

hop.declare_operators(open,goto, pick, place)
print('')
hop.print_operators(hop.get_operators())

def task1(state, r,o, x, y):
    return [('open',r, x),('goto',r, x, y), ('pick',r,o,y),('goto',r, y, x), ('place',r,o,x)]

#def task2(state, r,o,x,y):
    #return [('goto',r, x, y), ('pick',r,o,y), ('place',r,o,x)]

hop.declare_methods('task1',task1)
print('')
hop.print_methods(hop.get_methods())


state1 = hop.State('state1')
state1.loc ={'robot':'cupboard','coke':'table'}
state1.gripper = True           #False = it is closed   True = it is open
state1.cupDoorisopen = False    #False = it is closed   True = it is open

print("""
********************************************************************************
Call hop.plan(state1,[('task1','robot','coke','cupboard','table')])
********************************************************************************
""")



print('- If verbose=1, Pyhop also prints the intermediate states:')
hop.plan(state1,
         [('task1','robot','coke','cupboard','table')],
         hop.get_operators(),
         hop.get_methods(),
         verbose=1)

print('- If verbose=2, Pyhop also prints the intermediate states:')
hop.plan(state1,
         [('task1','robot','coke','cupboard','table')],
         hop.get_operators(),
         hop.get_methods(),
         verbose=2)

print('- If verbose=3, Pyhop also prints the intermediate states:')
hop.plan(state1,
         [('task1','robot','coke','cupboard','table')],
         hop.get_operators(),
         hop.get_methods(),
         verbose=3)
