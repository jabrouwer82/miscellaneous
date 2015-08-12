import random
import math

def genPoint():
  return (random.random(), random.random())

def testPoint(point):
  return math.pow(point[0], 2) + math.pow(point[1], 2) <= 1

def approxPi(sample_size, print_freq):
  inCircle = 0.0
  total = 0.0
  for x in xrange(sample_size):
    point = genPoint()
    if testPoint(point):
      inCircle += 1
    total += 1
    if x % print_freq == 0:
      pi = 4.0 * inCircle / total
      print str(x) + "        " + str(pi) + "       " + str(math.fabs(100.0 / math.pi * pi - 100.0)) + "%"
  return 4.0 * inCircle / total


pi = approxPi(1000000000, 1000000)
print str(pi) + "      " + str(math.fabs(100.0 / math.pi * pi - 100.0)) + "%"
