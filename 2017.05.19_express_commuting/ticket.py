import numpy
import random
import pandas as pd

random.seed(0)
numpy.set_printoptions(linewidth=200)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)

class Driver:
    id = None
    pct_ticket = 0

    def __init__(self, i, p):
        self.id = i
        self.pct_ticket = p

    def ticketed(self):
        return random.random() <= self.pct_ticket

    def __repr__(self):
        return '%s - %f' % (self.id, self.pct_ticket)

driver_input = list(zip(['a','b','c','d'],[0.1, 0.15, 0.2, 0.25]))
driver_map = {}
for d in driver_input:
    driver_map[d[0]] = Driver(d[0],d[1])
states = ['abcd', 'abc', 'abd', 'acd', 'bcd', 'ab', 'ac', 'ad', 'bc', 'bd', 'cd', 'a', 'b', 'c', 'd', '']

def calc_prob(s1,s2,drivers):
    set1 = set(list(s1))
    set2 = set(list(s2))
    if s1 == s2:
        if s1 == '':
            return 1
        else:
            return (1 - (1./len(s1)) * sum([drivers[x].pct_ticket for x in s1]))
    elif set1.issuperset(set2) and len(s1) == (len(s2) + 1):
        d = list(set1.difference(set2))[0]
        return (1./len(s1)) * drivers[d].pct_ticket
    else:
        return 0

def markov():
    P = numpy.zeros([len(states)]*2)
    for i1, s1 in enumerate(states):
        for i2, s2 in enumerate(states):
            P[i1][i2] = calc_prob(s1,s2,driver_map)
    return (P, solve(P))

def markov_simp():
    p = numpy.mean([0.1, 0.15, 0.2, 0.25])
    s = 1-p
    P = numpy.matrix([
        [s, p, 0, 0, 0],
        [0, s, p, 0, 0],
        [0, 0, s, p, 0],
        [0, 0, 0, s, p],
        [0, 0, 0, 0, 1]])
    return (P, solve(P))

def solve(P):
    N = len(P) - 1
    Q = P[0:N, 0:N]
    iQ = numpy.eye(N) - Q
    iQi = numpy.linalg.inv(iQ)
    row = iQi[0,0:N]
    if len(row) == 1:  #WTF is happening here?  markov_simp returns a 2d, but markov returns a 1d
        row = row.tolist()[0]
    return sum(row)

def sim():
    drivers = [Driver(x[0],x[1]) for x in driver_input]
    turn = 0
    while len(drivers) > 0:
        d = random.sample(drivers, 1)[0]
        if d.ticketed():
            drivers.remove(d)
        turn += 1
    return turn

if __name__ == '__main__':
    ms = markov_simp()
    m = markov()
    s = numpy.mean([sim() for x in range(100000)])

    states[-1] = '∅'
    MF = pd.DataFrame(m[0], index=states, columns=states)
    MS = pd.DataFrame(ms[0], index=list('43210'), columns=list('43210'))
    print('Markov Full:\n%s' % MF)
    print('\nMarkov Simp:\n%s' % MS)
    
    print('\nMarkov      = %f' % m[1])
    print('Markov_simp = %f' % ms[1])
    print('Simulated   = %f' % s)
