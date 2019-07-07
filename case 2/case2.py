from pyhop import hop
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

def open(state, r, x):
    if(state.gripperfree == True and state.loc[r] == x and state.cupboardisopen == False and state.isCupboard == True):
        state.cupboardisopen = True
        return state
    else:
        return False

#Compound tasks
# x:object y:location
def pick(state,r,o, y):
    # y = look_table(state, r)
    # while(state.objects[y] > 0):
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    if(state.gripperfree == True and state.loc[r] == y and state.objects[y]>0):
        state.gripperfree = False
        state.loc[o] = r
        state.objects[y] -= 1
        # place_on_tray(state, r, o)
    else:
        return False
    return state

# def place_on_tray(state, r, o):
#     if(state.loc[o] == r and state.gripperfree == False):
#         state.loc[o] = 'tray'
#         state.gripperfree = True
#         state.objects['tray'] += 1
#         return state
#     else:
#         return False


# def pick_from_tray(state, r, o):
#     if((state.loc[o] == 'tray' or state.loc[o] == 'cupboard') and state.gripperfree == True and state.loc[r] == 'cupboard'):
#         state.loc[o] = r
#         state.gripperfree = False
#         state.objects['tray'] -= 1
#         return state
#     else:
#         return False

def place(state,r,o, x):
    # print(state.objects['tray'])
    # pick_from_tray(state, r, o)
    if(state.loc[o] == r and state.gripperfree == False and state.loc[r]== x and state.cupboardisopen == True):
        state.gripperfree = True
        state.loc[o] = x
        state.objects['cupboard'] += 1
    else:
        return False
    return state


#initial state

hop.declare_operators(look_cupboard, open, look_table, goto, pick, place)
print('')
hop.print_operators(hop.get_operators())

#x and y are locations, o is object and r is robot
def task1(state, r, o, x, y):
    tasklist = [('look_cupboard',r), ('goto', r, '', x), ('open',r, x), ('look_table',r),('goto',r, x, y)]
    X1 = [('pick',r, o, y), ('goto',r, y, x), ('place',r,o,x), ('goto',r, x, y)]
    for k in range(5):
        for j in range(len(X1)):
            tasklist.append(X1[j])
    return tasklist

hop.declare_methods('task1',task1)
print('')
hop.print_methods(hop.get_methods())



state1 = hop.State('state1')
state1.loc = {'objects':'table', 'robot':''}
state1.objects = {'table': 5, 'cupboard': 0}
state1.gripperfree = True #gripper true referes to gripper free state
state1.cupboardisopen = False #cupboard is closed
state1.isTable = False
state1.isCupboard = False

print("""
********************************************************************************
Call hop.plan(state1,[('task1','robot','coke','cupboard','table')])
********************************************************************************
""")

print('- If verbose=3, Pyhop also prints the intermediate states:')
hop.plan(state1,
         [('task1','robot', 'objects', 'cupboard', 'table')],
         hop.get_operators(),
         hop.get_methods(),
         verbose=3)
