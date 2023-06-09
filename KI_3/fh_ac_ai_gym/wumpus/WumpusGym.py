import gym
from gym import error, spaces, utils
from gym.utils import seeding
from fh_ac_ai_gym.wumpus.WumpusWorld import Wumpus_World
from fh_ac_ai_gym.wumpus.WorldState import World_State, Action, Direction
import copy



class KnowledgeBase:
    def __init__(self, size):
        self.size = size
        self.sentences = {('-P00',)} #CNF ... and arr[i] and arr[i+1] and ..

    def registerBreezeAt(self,x,y):
        # Bxy
        self.sentences.add(('B'+str(x)+str(y),))
        self.sentences.add(('-P'+str(x)+str(y),))
        # Bxy <=> (Px+1,y || Px-1,y || Px,y+1 || Px,y-1) 

        # Bxy => (Px+1,y || Px-1,y || Px,y+1 || Px,y-1) &&
        # (Px+1,y || Px-1,y || Px,y+1 || Px,y-1) => Bxy

        # ((Px+1,y || Px-1,y || Px,y+1 || Px,y-1) || !Bxy) && 
        # (Bxy || (Px+1,y || Px-1,y || Px,y+1 || Px,y-1) )

        # (Px+1,y || Px-1,y || Px,y+1 || Px,y-1)

        tmp = []

        if(x < self.size - 1):
            tmp.append('P'+str(x+1)+str(y))
        if(y < self.size - 1):
            tmp.append('P'+str(x)+str(y+1))
        if(x > 0):
            tmp.append('P'+str(x-1)+str(y))
        if(y > 0):
            tmp.append('P'+str(x)+str(y-1))

        self.sentences.add(tuple(tmp))


    def registerNoBreezeAt(self,x,y):
        #-Bxy
        self.sentences.add(('-B'+str(x)+str(y),))
        self.sentences.add(('-P'+str(x)+str(y),))

        # Bxy <=> (Px+1,y || Px-1,y || Px,y+1 || Px,y-1) 

        # Bxy => (Px+1,y || Px-1,y || Px,y+1 || Px,y-1) &&
        # (Px+1,y || Px-1,y || Px,y+1 || Px,y-1) => Bxy

        # !(Px+1,y || Px-1,y || Px,y+1 || Px,y-1) 

        #  (!Px+1,y && !Px-1,y && !Px,y+1 && !Px,y-1) 

        if(x < self.size - 1):
            self.sentences.add(('-P'+str(x+1)+str(y),))
        if(y < self.size - 1):
            self.sentences.add(('-P'+str(x)+str(y+1),))
        if(x > 0):
            self.sentences.add(('-P'+str(x-1)+str(y),))
        if(y > 0):
            self.sentences.add(('-P'+str(x)+str(y-1),))

            
    def registerStenchAt(self,x,y):
        # Sxy
        self.sentences.add(('S'+str(x)+str(y),))
        # Sxy <=> (Wx+1,y || Wx-1,y || Wx,y+1 || Wx,y-1) 

        tmp = []

        if(x < self.size - 1):
            tmp.append('W'+str(x+1)+str(y))
        if(y < self.size - 1):
            tmp.append('W'+str(x)+str(y+1))
        if(x > 0):
            tmp.append('W'+str(x-1)+str(y))
        if(y > 0):
            tmp.append('W'+str(x)+str(y-1))

        self.sentences.add(tuple(tmp))

    def registerNoStenchAt(self,x,y):
        # -Sxy
        self.sentences.add(('-S'+str(x)+str(y),))
        self.sentences.add(('-W'+str(x)+str(y),))

        # -Sxy <=> -(Px+1,y || Px-1,y || Px,y+1 || Px,y-1) 


        if(x < self.size - 1):
            self.sentences.add(('-W'+str(x+1)+str(y),))
        if(y < self.size - 1):
            self.sentences.add(('-W'+str(x)+str(y+1),))
        if(x > 0):
            self.sentences.add(('-W'+str(x-1)+str(y),))
        if(y > 0):
            self.sentences.add(('-W'+str(x)+str(y-1),))


    def tell(self, perception):
        x = perception['x']
        y = perception['y']

        if(perception['breeze']):
            self.registerBreezeAt(x,y)
        else:
            self.registerNoBreezeAt(x,y)
        if(perception['stench']):
            self.registerStenchAt(x,y)
        else:
            self.registerNoStenchAt(x,y)

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

        if(self.resolution('P'+str(x)+str(y))):
            value.append('Pit')
        elif(not self.resolution('-P'+str(x)+str(y))):
            value.append('?Pit')
        if(self.resolution('W'+str(x)+str(y))):
            value.append('Wumpus')
        elif(not self.resolution('-W'+str(x)+str(y))):
            value.append('?Wumpus')

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
