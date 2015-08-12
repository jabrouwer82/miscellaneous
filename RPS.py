import random

class Player():
  def __init__(self, name):
    self.name = name
    self.wins = 0
    self.losses = 0
  
  def diff(self):
    return self.wins - self.losses

  def percent(self):
    if self.wins + self.losses:
      return int((100.0 * self.wins) / (self.wins + self.losses))
    else:
      return 0

  def total(self):
    return self.wins + self.losses

  def score(self):
    return (self.percent() / 100.0) * self.wins - ((100 - self.percent()) / 100.0) * self.losses

  def __str__(self):
    return self.name + '\t' + str(self.total()) + '\t' + str(self.wins) + '\t' + str(self.losses) + '\t' + str(self.percent()) + '\t' + str(self.diff()) + '\t' + str(self.score())


players = []
for i in xrange(20):
  t = Player('p' + str(i))
  players.append(t)
                         
for player in players:
  for i in xrange(1000):
    pplay = random.randint(1, 3)
    cplay = random.randint(1, 3)
    if pplay - cplay % 3 == 1:
      player.wins += 1
    elif pplay - cplay % 3 == 2:
      player.losses += 1


print 'Name\tTotal\tWins\tLosses\tPercent\tDiff\tScore'
players = sorted(players, reverse=True, key=lambda player: player.score())
for player in players:
  print player
