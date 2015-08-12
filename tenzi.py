import random

NUM_DICE = 10
DICE_SIDES = 6

def roll(n):
  ret = []
  for i in range(n):
    ret.append(random.randint(1, DICE_SIDES))
  #print('Rolled: {}'.format(ret))
  return ret

def reduce_roll(rolls, n):
  return [roll for roll in rolls if roll != n]

def play_random_goal():
  goal = random.randint(1, DICE_SIDES)
  return play(goal)

def play_best_first_roll():
  rolls = roll(NUM_DICE)
  best_num = 1
  best_count = NUM_DICE + 1
  for n in range(1, DICE_SIDES + 1):
    post_roll = reduce_roll(rolls, n)
    if len(post_roll) < best_count:
      best_num = n
      best_count = len(post_roll)
  return play(goal=best_num, num_roll=1, num_dice=best_count)
  
def play(goal=None, num_roll=0, num_dice=NUM_DICE):
  #print('Goal is: {}'.format(goal))
  num_rolls = 0
  while num_dice > 0:
    dice = roll(num_dice)
    post_roll = reduce_roll(dice, goal)
    num_rolls += 1
    num_dice = len(post_roll)
  #print('Won in {} rolls'.format(num_rolls))
  return num_rolls

if __name__ == '__main__':
  num_games = 0
  count_turns = 0
  for n in range(100000):
    count_turns += play_best_first_roll()
    num_games += 1
  print('It took on average {} to win with strategy'.format(count_turns/num_games))
  num_games = 0
  count_turns = 0
  for n in range(100000):
    count_turns += play_random_goal()
    num_games += 1
  print('It took on average {} to win with a random goal'.format(count_turns/num_games))
