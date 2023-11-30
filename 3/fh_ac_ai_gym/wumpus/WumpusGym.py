import gym
from gym import error, spaces, utils
from gym.utils import seeding
from fh_ac_ai_gym.wumpus.WumpusWorld import Wumpus_World
from fh_ac_ai_gym.wumpus.WorldState import World_State, Action, Direction
import queue



class KnowledgeBase:
    def __init__(self, size):
        self.size = size
        self.sentences = {('-P00',),('-W00',)} #CNF ... and arr[i] and arr[i+1] and ..
        self.firstMethod = False


    def registerConjuctionAdjacent(self,e,x,y):
        if(x < self.size - 1):
            self.sentences.add((e+str(x+1)+str(y),))
        if(y < self.size - 1):
            self.sentences.add((e+str(x)+str(y+1),))
        if(x > 0):
            self.sentences.add((e+str(x-1)+str(y),))
        if(y > 0):
            self.sentences.add((e+str(x)+str(y-1),))

    def registerDisjuctionAdjacent(self,e,x,y):
        tmp = []
        if(x < self.size - 1):
            tmp.append(e+str(x+1)+str(y))
        if(y < self.size - 1):
            tmp.append(e+str(x)+str(y+1))
        if(x > 0):
            tmp.append(e+str(x-1)+str(y))
        if(y > 0):
            tmp.append(e+str(x)+str(y-1))
        self.sentences.add(tuple(tmp))

    def registerHornClauses(self,e1,e2,x,y):
        tmp = []
        tmp2 = []
        tmp.append(e1+str(x)+str(y))
        tmp2.append(e1+str(x)+str(y))

        if(x < self.size - 1):
            tmp.append('-'+e1+str(x+1)+str(y))
        if(x > 0):
            tmp.append('-'+e1+str(x-1)+str(y))
        if(y < self.size - 1):
            tmp2.append('-'+e1+str(x)+str(y+1))
        if(y > 0):
            tmp2.append('-'+e1+str(x)+str(y-1))

        save1 = tmp.copy()
        save2 = tmp2.copy()

        if(y < self.size - 1):
            tmp.append('-'+e1+str(x)+str(y+1))
            self.sentences.add((tuple(tmp),(e2+str(x)+str(y+1),)))
            if(y > 0):
                self.sentences.add((tuple(tmp),(e2+str(x)+str(y-1),)))
        if(y > 0):
            save1.append('-'+e1+str(x)+str(y-1))
            self.sentences.add((tuple(save1),(e2+str(x)+str(y-1),)))
            if(y < self.size - 1):
                self.sentences.add((tuple(save1),(e2+str(x)+str(y+1),)))

        if(x < self.size - 1):
            tmp2.append('-'+e1+str(x+1)+str(y))
            self.sentences.add((tuple(tmp),(e2+str(x+1)+str(y),)))
            if(x > 0):
                self.sentences.add((tuple(tmp),(e2+str(x-1)+str(y),)))
        if(x > 0):
            save2.append('-'+e1+str(x-1)+str(y))
            self.sentences.add((tuple(save2),(e2+str(x-1)+str(y),)))
            if(x < self.size - 1):
                self.sentences.add((tuple(save2),(e2+str(x+1)+str(y),)))
    
    def registerAdjacentHornClauses(self,t,p,x,y):
        if(x < self.size - 1):
            self.sentences.add(((p+str(x)+str(y),),(t+str(x+1)+str(y),)))
        if(y < self.size - 1):
            self.sentences.add(((p+str(x)+str(y),),(t+str(x)+str(y+1),)))
        if(x > 0):
            self.sentences.add(((p+str(x)+str(y),),(t+str(x-1)+str(y),)))
        if(y > 0):
            self.sentences.add(((p+str(x)+str(y),),(t+str(x)+str(y-1),)))

    def tell(self, perception):
        x = perception['x']
        y = perception['y']


        if(self.firstMethod):
            # Bxy <=> (Px+1,y || Px-1,y || Px,y+1 || Px,y-1) 
            # -Bxy <=> (-Px+1,y && -Px-1,y && -Px,y+1 && -Px,y-1)
            if(perception['breeze']):
                self.sentences.add(('B'+str(x)+str(y),))
                self.sentences.add(('-P'+str(x)+str(y),))
                self.registerDisjuctionAdjacent('P',x,y)
            else:
                self.sentences.add(('-B'+str(x)+str(y),))
                self.registerConjuctionAdjacent('-P',x,y)
            # Sxy <=> (Wx+1,y || Wx-1,y || Wx,y+1 || Wx,y-1) 
            # -Sxy <=> (-Wx+1,y && -Wx-1,y && -Wx,y+1 && -Wx,y-1)
            if(perception['stench']):
                self.sentences.add(('S'+str(x)+str(y),))
                self.sentences.add(('-W'+str(x)+str(y),))
                self.registerDisjuctionAdjacent('W',x,y)
            else:
                self.sentences.add(('-S'+str(x)+str(y),))
                self.registerConjuctionAdjacent('-W',x,y)
        else:
            if(x < self.size - 1):
                self.registerHornClauses('B','P',x+1,y)
                self.registerHornClauses('S','W',x+1,y)
            if(y < self.size - 1):
                self.registerHornClauses('B','P',x,y+1)
                self.registerHornClauses('S','W',x,y+1)
            if(x > 0):
                self.registerHornClauses('B','P',x-1,y)
                self.registerHornClauses('S','W',x-1,y)
            if(y > 0):
                self.registerHornClauses('B','P',x,y-1)
                self.registerHornClauses('S','W',x,y-1)
            if(perception['breeze']):
                self.sentences.add(('B'+str(x)+str(y),))
            else:
                self.sentences.add(('-B'+str(x)+str(y),))
                self.registerConjuctionAdjacent('-P',x,y)
            if(perception['stench']):
                self.sentences.add(('S'+str(x)+str(y),))
            else:
                self.sentences.add(('-S'+str(x)+str(y),))
                self.registerConjuctionAdjacent('-W',x,y)


    def forwardChaining(self, query):
        count = {}
        inferred = {}
        agenda = queue.Queue()
        
        for item in self.sentences:
            if(len(item) == 1):
                agenda.put(item)
                inferred[item] = False
                if(item[0] == query):
                    return True
                if(item[0] == '-'+query):
                    return False
            else: 
                for items in item:
                        inferred[items] = False
                count[item[0]] = 0
                for items in item[0]:
                    count[item[0]] += 1

        while not agenda.empty():
            current = agenda.get()
            if(current == (query,)):
                return True
            if(not inferred[current]):
                inferred[current] = True
                for item in self.findAllPremises(current):
                    count[item] -= 1
                    if(count[item] == 0):
                        for add in self.findAllConclusion(item):
                            agenda.put(add)
        return False

    def findAllPremises(self,q):
        result = set()
        for item in self.sentences:
            if(len(item) == 2):
                for i in item[0]:
                    if((i,) == q):
                        result.add(item[0])
                        break
        return result

    def findAllConclusion(self,q):
        result = set()
        for item in self.sentences:
            if(len(item) == 2 and item[0] == q):
                result.add(tuple(item[1]))
        return result

    def resolve(self, c1, c2):
        result = set()
        combined = {c1} | {c2}
        for item1 in c1:
            for item2 in c2:
                if(item1 and item2 and item1 == '-'+item2 or item2 == '-'+item1):
                    for x in combined:
                        tmp = []
                        for y in x:
                            if(y != item1 and y != item2):
                                tmp.append(y)
                        if(len(tmp) == 0):
                            result.add(tuple())
                        else:
                            result.add(tuple(tmp))
        if(result):
            return result
        return combined


    def resolution(self,query):
        query =  query[1:] if (query[0] == '-') else ('-'+query)
        clauses = self.sentences.copy()
        clauses.add((query,))
        new = set()

        while(True):
            for i in range(len(clauses)):
                for j in range(len(clauses)):
                    if(j == i):
                        continue
                    C1 = list(clauses)[i]
                    C2 = list(clauses)[j]

                    if(isinstance(C1, str)):
                         C1 = (C1,)
                    if(isinstance(C2, str)):
                        C2 = (C2,)


                    resolvent = self.resolve(C1,C2)

                    if(() in resolvent and len(resolvent) == 1):    ##hereeeeee
                        return True
                    
                    new |= resolvent
            if(new <= clauses):
                return False
            clauses |= new
            

    def ask(self, x,y):
        value = []

        if(self.firstMethod):
            if(self.resolution('P'+str(x)+str(y))):
                value.append('Pit')
            elif(not self.resolution('-P'+str(x)+str(y))):
                value.append('?Pit')
            if(self.resolution('W'+str(x)+str(y))):
                value.append('Wumpus')
            elif(not self.resolution('-W'+str(x)+str(y))):
                value.append('?Wumpus')
            if(len(value) == 0):
                value.append('OK') 
        else:
            if(self.forwardChaining('P'+str(x)+str(y))):
                value.append('Pit')
            elif(not self.forwardChaining('-P'+str(x)+str(y))):
                value.append('?Pit')
            if(self.forwardChaining('W'+str(x)+str(y))):
                value.append('Wumpus')
            elif(not self.forwardChaining('-W'+str(x)+str(y))):
                value.append('?Wumpus')
            if(len(value) == 0):
                value.append('OK') 
        return ','.join(value)



class WumpusWorldEnv(gym.Env):
    metadata = {'render.modes' : ['human']}
    def __init__(self, size=4):
        self.size = size
        self.KB = KnowledgeBase(size)
        self._world = Wumpus_World(size)
        self.action_space = [0,1,2,3,4,5]

    def step(self, action):
        done = self._world.exec_action(action)
        obs = self._world.get_observation()
        reward = self._world.get_reward()
        self.KB.tell(obs)
        return obs, reward, not done, {"info", "no further information"}

    def reset(self):
        self._world.reset()
        return self._world.get_observation()

    def render(self, mode='human'):
        self._world.print()
        print("Knowledge Base: ")
        x = self._world.state.agent_location.x
        y = self._world.state.agent_location.y
        print("Current: ", self.KB.ask(x,y));
        if(x < self.size - 1):
            print("Walk Right: ", self.KB.ask(x + 1, y))
        if(y < self.size - 1):
            print("Walk Above: ", self.KB.ask(x, y + 1))
        if(x > 0):
            print("Walk Left: ", self.KB.ask(x - 1, y))
        if(y > 0):
            print("Walk Below: ", self.KB.ask(x, y - 1))


    def close(self):
        print("Not necessary since no seperate window was opened")
        pass
