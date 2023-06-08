import gym
from gym import error, spaces, utils
from gym.utils import seeding
from fh_ac_ai_gym.wumpus.WumpusWorld import Wumpus_World
from fh_ac_ai_gym.wumpus.WorldState import World_State, Action, Direction
import copy



class KnowledgeBase:
    def __init__(self, size):
        self.size = size
        self.wumpus_death = False
        self.gold_collected = False
        self.sentences = {('-P00',)} #CNF ... and arr[i] and arr[i+1] and ..

    def registerBreezeAt(self,x,y):
        # Bxy
        self.sentences.add(('B'+str(x)+str(y),))
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

        # Bxy <=> (Px+1,y || Px-1,y || Px,y+1 || Px,y-1) 

        # Bxy => (Px+1,y || Px-1,y || Px,y+1 || Px,y-1) &&
        # (Px+1,y || Px-1,y || Px,y+1 || Px,y-1) => Bxy

        # !(Px+1,y || Px-1,y || Px,y+1 || Px,y-1) 

        #  (!Px+1,y && !Px-1,y && !Px,y+1 && !Px,y-1) 

        if(x < self.size - 1):
            self.sentences.add(('P'+str(x+1)+str(y),))
        if(y < self.size - 1):
            self.sentences.add(('P'+str(x)+str(y+1),))
        if(x > 0):
            self.sentences.add(('P'+str(x-1)+str(y),))
        if(y > 0):
            self.sentences.add(('P'+str(x)+str(y-1),))

            
    def tell(self, perception):
        x = perception['x']
        y = perception['y']

        if(perception['scream']):
            self.wumpus_death = True
        if(perception['gold']):
            self.gold_collected = True
        if(perception['breeze']):
            self.registerBreezeAt(x,y)
        else:
            self.registerNoBreezeAt(x,y)
        if(perception['stench']):
            pass

    def resolve(self, c1, c2):
        result = set()
        combined = c1 | c2
        for item1 in c1:
            for item2 in c2:
                if(item1 == '-'+item2 or item2 == '-'+item1):
                    tmp = [x for x in combined if (x != item1 and x != item2)]
                    result.add(tuple(tmp))
        if(result == {}):
            return combined
        return result


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
                    C1 = list(clauses)[len(clauses) - 1 - i]
                    C2 = list(clauses)[len(clauses) - 1 - j]
                    resolvent = self.resolve(set(C1), set(C2))

                    if(() in resolvent):
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
            value.append('Pit?')

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
