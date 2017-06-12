_You’re on a game show, and you’re asked to sit down at a table covered with sealed envelopes. You are told that each envelope contains a check for an amount of money, each amount different from all the others, but you are given no other information about the distribution of amounts. (As far as you know, the biggest check on the table could be $1.06 or it could be $98,765,432,100.00.) You may pick an envelope, open it and read the amount of the check. You can then either keep that check, ending the game, or toss it away permanently and open another envelope. You can then keep that second check or toss it away and open a third envelope. And then you can keep the third check or throw it away and pick a fourth envelope. But that’s it — if you open a fourth envelope, you have to keep that check, no matter how paltry it is._

_What strategy should you follow to maximize your chances of getting a nice payday?_

### Solution

Opening one envelope and stopping is no better than randomly choosing an envelope to stop at, so we know that a better or equal strategy exists.  Let the envelope amounts be called A, B, C, D, where A < B < C < D.  Let our envelopes that we open on turns 1 - 4 be called E1, E2, E3, E4.

Open the first two.  

### E2 > E1

If E2 > E1 then we know one of the following must have happened:

* A - B
* A - C
* A - D
* B - C
* B - D
* C - D

Giving us the following likelihood for E2's prize and chances of improving

| Envelope | likelihood | chances of improving by<br>opening a 3rd envelope |
| -------- | ---------- | ------------------------------------------------- |
| B | 1/6 | 100% |
| C | 2/6 | 50% |
| D | 3/6 | 0% |

We only have a 1 in 6 chance of being guaranteed improvement going forward (B), while we have a 3 in 6 chance of being guaranteed to decline (D).  (C) represents a neutral choice.  Therefore we should quit.

### E2 < E1

Conversely, If E2 < E1, then one of the following happened:

* D - C
* D - B
* D - A
* C - B
* C - A
* B - A

yielding:

| Envelope | likelihood | chances of improving by<br>opening a 3rd envelope |
| -------- | ---------- | ------------------------------------------------- |
| A | 3/6 | 100% |
| B | 2/6 | 50% |
| C | 1/6 | 0% |

So we should keep going.

### E3 < E2 < E1

One of the following happened:

* D - C - B
* D - C - A
* D - B - A
* C - B - A

| Envelope | likelihood | chances of improving by<br>opening a 4th envelope |
| -------- | ---------- | ------------------------------------------------- |
| A | 3/4 | 100% |
| B | 1/4 | 0% | 

So we should obviously keep going and pick the final envelope.

###  E2 < E3 < E1

One of the following happened:

* D - B - C
* D - A - C
* D - A - B
* C - A - B

| Envelope | likelihood | chances of improving by<br>opening a 4th envelope |
| -------- | ---------- | ------------------------------------------------- |
| C | 2/4 | 50% |
| B | 2/4 | 50% |

So we can either continue or stop.  For ease of summarizing the overal strategy, we will stop.

###  E2 < E1 < E3

One of the following happened:

* B - A - C
* B - A - D
* C - A - D
* C - B - D

| Envelope | likelihood | chances of improving by<br>opening a 4th envelope |
| -------- | ---------- | ------------------------------------------------- |
| C | 1/4 | 100% |
| D | 3/4 | 0% |

So we should stop.

### Summary

Stop whenever you pick an evelope that is greater than any previous choice.

### Testing

I created a script that enumerates all possible strategies by exploring all possible decision combinations:

![decision tree](https://github.com/nabraham/538-riddler/raw/master/2017.06.09_classic_payout/Envelopes.png)

D = draw, P = stop, S = Smallest, M = Medium, L = Large

Green nodes represent places where we have an option to stop or continue.  The numbers are the node id used in the [python script](./payout.py).  I generated 10,000* test sets and ran them accros all 82 unique strategies.  Here are the top  5 scoring strategies:

```
0.886300: (1, 3)-(4, 7)-(5, 8)-(10, 17)-(11, 19)-(12, 20)
0.894300: (1, 3)-(4, 7)-(5, 8)-(10, 17)-(11, 18)-(12, 20)
1.064200: (1, 3)-(4, 7)-(5, 9)-(10, 17)-(11, 19)-(12, 20)-(13, 23)-(14, 25)-(15, 26)
1.067100: (1, 3)-(4, 7)-(5, 9)-(10, 17)-(11, 19)-(12, 20)-(13, 23)-(14, 24)-(15, 26)
1.072200: (1, 3)-(4, 7)-(5, 9)-(10, 17)-(11, 18)-(12, 20)-(13, 23)-(14, 25)-(15, 26)
```
The score (before the colon) is the average position of the prize chosen from biggest to smallest:

* D = 0
* C = 1
* B = 2
* A = 3

As predicted, the best scoring strategy is the one that stops whenever we see a bigger number.  The pairs on the right side of the colon are the edges at decision points in the strategy.  The worst strategy turned out to be:

```
2.124500: (1, 3)-(4, 6)-(5, 9)-(13, 22)-(14, 24)-(15, 27)
```
Which is stop drawing after you encounter a smaller prize.


*slightly less than 10,000 due to duplicates
