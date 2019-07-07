#case 3 : To perceive and pick objects
import time 
from pyhop import hop
start = time.time()
# Primitive tasks
# goto from location x to location y
def goto(state, r, x, y):
    if state.loc[r] == x:
        state.loc[r] = y
        return state
    else:
        return False

def look_table(state, r):
    state.isTable = True
    return state

def look_cupboard(state, r):
    state.isCupboard = True
    return state

def perceiveObjects(state, x, i): #x is table
    print("Here------------------------------------")
    state.loc['objects'] = x #setting the location of objects as table
    state.objects[x] = len(state.objectsLocation) #updating the number of objects on table
    key_objects = state.objectsLocation.keys()
    # state.perceiveObjectsonTable.append(key_objects)
    print("x is", x)
    return state


def open(state, r, x):
    if(state.gripperfree == True and state.loc[r] == x and state.cupboardisopen == False and state.isCupboard == True):
        state.cupboardisopen = True
        return state
    else:
        return False

#Compound tasks
# x:object y:location
def pick(state,r,o, y, i): # y - table and r - robot
    objs = state.objectsLocation
    key_objects = objs.keys()
    if(state.gripperfree == True and state.loc[r] == y and state.objects[y]>0):
        state.gripperfree = False
        objs[key_objects[state.i]] = r #objects on table are picked
        state.objects[y] -= 1 #just specifies number of objects
    else:
        return False
    return state

def place(state,r,o, x, i):
    objs = state.objectsLocation
    key_objects = objs.keys()
    if(key_objects[state.i] in state.category1):
        if(objs[key_objects[state.i]] == r and state.gripperfree == False and state.loc[r]== x and state.cupboardisopen == True and len(state.category1) > 0):
            state.gripperfree = True
            state.loc[o] = x
            state.objects[x] += 1
            state.objects['shelf_1'] += 1
            state.objectsLocation[key_objects[state.i]] = 'shelf_1'
            state.category1.remove(key_objects[state.i])
        else:
            return False
    if(key_objects[state.i] in state.category2):
        if(objs[key_objects[state.i]] == r and state.gripperfree == False and state.loc[r]== x and state.cupboardisopen == True and len(state.category2) > 0):
            state.gripperfree = True
            state.loc[o] = x
            state.objects[x] += 1
            state.objects['shelf_2'] += 1
            state.objectsLocation[key_objects[state.i]] = 'shelf_2'
            state.category2.remove(key_objects[state.i])
        else:
            return False
    # objs[key_objects[state.i]] = x
    state.i += 1
    # state.loc['objects'] = 'cupboard'
    state.isTable = False
    return state

#initial state
hop.declare_operators(look_cupboard, open, look_table, goto, pick, place, perceiveObjects)
print('')
hop.print_operators(hop.get_operators())


#x and y are locations, o is object and r is robot
def task1(state, r, o, x, y, i):
    tasklist = [('look_cupboard',r), ('goto', r, '', x), ('open',r, x), ('look_table',r), ('goto',r, x, y), ('perceiveObjects', y, i)]
    X1 = [('pick',r, o, y, i), ('goto',r, y, x), ('place',r,o,x, i), ('goto',r, x, y)]
    for k in range(len(state.objectsLocation)):
        for j in range(len(X1)):
            tasklist.append(X1[j])
    return tasklist

hop.declare_methods('task1',task1)
print('')
hop.print_methods(hop.get_methods())

# hop.declare_methods('task2',task2)
# print('')
# hop.print_methods(hop.get_methods())

state1 = hop.State('state1')
state1.loc = {'objects':'', 'robot':''}
state1.objectsLocation = {'coke':'', 'pepsi':'', 'apple':'', 'lemon':'', 'orange': ''}
state1.category1 = ['coke', 'pepsi']
state1.category2 = ['apple', 'lemon', 'orange']
state1.objects = {'table': 0, 'cupboard': 0, 'shelf_1': 0, 'shelf_2':0}
state1.gripperfree = True #gripper true referes to gripper free state
state1.cupboardisopen = False #cupboard is closed
state1.isTable = False
state1.isCupboard = False
state1.i = 0

print("""
********************************************************************************
Call hop.plan(state1,[('task1','robot','coke','cupboard','table')])
********************************************************************************
""")

print('- If verbose=2, Pyhop also prints the intermediate states:')
# hop.plan(state1,
#          [('task1','robot', 'objects', 'cupboard', 'table')],
#          hop.get_operators(),
#          hop.get_methods(),
#          verbose=3)

hop.seek_plan(state1,
         [('task1', 'robot','objects','cupboard','table', 0)],
         hop.get_operators(),
         hop.get_methods(),[],0,
         verbose=3)
# hop.plan(state1,
#          [('task2','robot', 'objects', 'cupboard', 'table')],
#          hop.get_operators(),
#          hop.get_methods(),
#          verbose=3)
