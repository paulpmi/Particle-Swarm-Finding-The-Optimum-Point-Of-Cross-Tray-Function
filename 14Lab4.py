from random import randint
from random import random
import math

class Particle:
    def __init__(self):
        self.pos = [randint(-10, 10) for _ in range(2)]
        self.velocity = 0
        self.fitness = self.evaluate()
        self.bestPosition = self.pos
        self.bestFitness = self.fitness
     

    def evaluate(self):
        x = self.pos[0]
        y = self.pos[1]
        function = -0.0001*math.pow((abs(math.sin(x)*math.sin(y)*math.exp(100-(math.sqrt(abs((math.pow(x, 2+math.pow(y,2))))/math.pi)))))+1,0.1)
        return function

    def update(self,particle):
        s = 1 / (1 + math.pow((math.exp(1)), -particle.velocity))
        for i in range(2):
            if (random() > s):
                self.pos[i] = randint(-10, 10)
            self.fitness = self.bestFitness

class Swarm:
    def __init__(self):
        self.v=[Particle() for i in range(40)] #list of particles
        self.numberOfParticles = 40
        #print(self.v[1].pos)

    def getBestNeighbour(self,particle):
        return particle

    def getBestParticles(self):
        s = sorted(self.v, key = lambda x:x.evaluate(), reverse=True)
        self.v = s
        return s[-1]


class Controller:
    
    def __init__(self, population):
        self.population = population
        self.fileName = 'parameters.txt'

    def iteration(self):
        best = 0
        inertia = 0.5
        clf = 0.4
        slf = 0.5
        new_velocity = 0
        for i in range(len(self.population.v)):
            if self.population.v[i].bestFitness > self.population.v[best].bestFitness:
                best = i
        for i in range(len(self.population.v)):
            new_velocity = inertia * self.population.v[i].velocity
            new_velocity += clf * random() * (sum(self.population.v[i].bestPosition) - sum(self.population.v[i].pos))
            new_velocity += slf * random() * (sum(self.population.v[best].bestPosition) - sum(self.population.v[i].pos))
            trial = sum(self.population.v[i].pos) + new_velocity
            aux = self.population.v[best]
            if trial > 0 and trial < 7: 
                new_velocity = self.population.v[i].velocity
                #new_velocity = 0
                aux = self.population.v[i]
            self.population.v[i].velocity = new_velocity
            #print(self.population.v[i].pos, " before update ")
            self.population.v[i].update(aux)
            #print(self.population.v[i].pos, " after update ")
        return self.population.getBestParticles()


    def runAlg(self, nu):
        a = self.iteration()
        for _ in range(nu):
            a = self.iteration()
            #self.population = Swarm()
        return a

    def loadParameters(self):
        with open(self.fileName, 'r') as f:
            self.n = int(f.readline().strip())
        f.close()


def mean(l):
        s=0
        n=len(l)
        for i in l:
            s+=i
        return s/n
        print("Mean:", s/n)

#standard deviation
def standardDev(l):
    s = 0;
    m = mean(l)
    for i in l:
        s=s+(i - m) **2
    return math.sqrt(s/(len(l)))

def m():
    l = []
    s = Swarm()
    c = Controller(s)
    
    for i in range(0,30):
        a= c.runAlg(i)
        print("Best", a.pos)
        l.append(a.bestFitness)
    print("Mean:", mean(l))
    print("Standard deviation:", standardDev(l))


def main():
    s = Swarm()
    c = Controller(s)
    c.runAlg(40)

    m()
main()