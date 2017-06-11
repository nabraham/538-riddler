import itertools
import random
from collections import defaultdict

def create_nodes():
    return dict([ (1, 'D'), (2, 'P'), (3, 'D'), (4, 'S'), (5, 'L'), (6, 'P'), (7, 'D'),
    (8, 'P'), (9, 'D'), (10, 'S'), (11, 'M'), (12, 'L'), (13, 'S'), (14, 'M'),
    (15, 'L'), (16, 'P'), (17, 'D'), (18, 'P'), (19, 'D'), (20, 'P'), (21, 'D'),
    (22, 'P'), (23, 'D'), (24, 'P'), (25, 'D'), (26, 'P'), (27, 'D')]) 

def create_strategy(c1,c4,c5,c10,c11,c12,c13,c14,c15):
    children = defaultdict(list)
    name = [(1,c1)]
    children[1].append(c1)
    if c1 == 2:
        return (str(name[0]), children)
    children[3].append(4)
    children[3].append(5)
    children[4].append(c4)
    name.append((4,c4))
    children[5].append(c5)
    name.append((5,c5))
    if c4 == 7:
        children[7].append(10)
        children[7].append(11)
        children[7].append(12)
        children[10].append(c10)
        children[11].append(c11)
        children[12].append(c12)
        name += [(10,c10),(11,c11),(12,c12)]
    if c5 == 9:
        children[9].append(13)
        children[9].append(14)
        children[9].append(15)
        children[13].append(c13)
        children[14].append(c14)
        children[15].append(c15)
        name += [(13,c13),(14,c14),(15,c15)]
    return ('-'.join(map(str,name)), children)

def is_smallest(val, arr):
    return val < min(arr)

def is_largest(val, arr):
    return val > max(arr)

def is_middle(val, arr):
    return len(arr) == 2 and val < max(arr) and val > min(arr)

def evaluate_strategy(children, nodes, envelopes):
    node = 1
    val = -1
    index = 0
    instruction = None
    seen = []
    while index < 4:
        #print('Node: %s, Val: %s, Index: %s, seen: %s' % tuple(map(str, [node, val, index, seen])))
        instruction = nodes[node]
        if instruction == 'P':
            break
        elif instruction == 'D':
            val = envelopes[index]
            index += 1
            if len(children[node]) == 0:
                break
            elif len(children[node]) == 1:
                node = children[node][0]
            else:
                nextNode = None
                for c in children[node]:
                    if nodes[c] == 'S' and is_smallest(val, seen):
                        nextNode = children[c][0]
                    elif nodes[c] == 'M' and is_middle(val, seen):
                        nextNode = children[c][0]
                    elif nodes[c] == 'L' and is_largest(val, seen):
                        nextNode = children[c][0]
                if nextNode == None:
                    raise Exception('Not falling to SML case')
                node = nextNode
            seen.append(val)
    return (index, val)

def create_strategies():
    C1 = [2,3]
    C4 = [6,7]
    C5 = [8,9]
    C10 = [16,17]
    C11 = [18,19]
    C12 = [20,21]
    C13 = [22,23]
    C14 = [24,25]
    C15 = [26,27]

    strategies = {}
    for p in itertools.product(C1,C4,C5,C10,C11,C12,C13,C14,C15):
        (n, s) = create_strategy(*p)
        if n not in strategies:
            strategies[n] = s
    return strategies

def create_test_set(n):
    E = []
    for i in range(n):
        bound = random.randint(10,10000000)
        s = set([random.randint(0,bound) for x in range(4)])
        if len(s) == 4:
            E.append(list(s))
    return E

def update_scores(scores, name, val, envelopes):
    s_env = sorted(envelopes, reverse=True)
    i = s_env.index(val)
    scores[name].append(i)

def main():
    random.seed(0)
    test_set = create_test_set(10000)
    nodes = create_nodes()
    strategies = create_strategies()
    scores = defaultdict(list)
    for e, envelopes in enumerate(test_set):
        for strat_name in strategies:
            #print('\nEvaluating '  + strat_name + '(%d)' % e)
            (i,v) = evaluate_strategy(strategies[strat_name], nodes, envelopes)
            update_scores(scores, strat_name, v, envelopes)

    score_list = []
    for name in scores:
        score_list.append((sum(scores[name]) / len(scores[name]), name))
    score_list.sort(key=lambda x: x[0])
    print('\n'.join(map(lambda x: '%f: %s' % x, score_list)))

if __name__ == '__main__':
    main()
