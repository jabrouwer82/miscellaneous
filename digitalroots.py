from itertools import combinations

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def digital_root(nums):
  # Concatenate the ints in a string
  nums = ''.join(map(str, nums))
  root = 0
  for num in nums:
    root += int(num)
  if len(str(root)) > 1:
    return digital_root([root])
  else:
    return root

def splits(digits, prev_groups=(), groupings=()):
  if not groupings:
    groupings = []
  #print('Args {}'.format(groupings))
  combs = [combinations(digits, length) for length in range(3, 6)]
  # Flatten the list of lists
  combs = [elem for comb_list in combs for elem in comb_list]
  #print('Combs {}'.format(combs))
  for comb in combs:
    rem_digits = list_sub(digits, comb)
    groups = list(prev_groups)
    groups.append(Group(comb))
    groupings = splits(rem_digits, prev_groups=groups, groupings=groupings)
  if not combs:
    groups = prev_groups
    if digits:
      groups = list(prev_groups)
      groups.append(Group(digits))
    #print(groups)
    groupings.append(Grouping(groups))
  return groupings
  
def filter_splits(digits, targets=(), strict=False, only_valid=False):
  groupings = splits(digits)
  if only_valid:
    groupings = [grouping for grouping in groupings if len(grouping.invalid_groups) == 0]
  filtered_groupings = []
  
  if targets and not strict:
    for grouping in groupings:
      match = False
      for group in grouping.valid_groups:
        if group.root in targets:
          match = True
      if match:
        filtered_groupings.append(grouping)

  if targets and strict:
    for grouping in groupings:
      missing = False
      for group in grouping.valid_groups:
        if group.root not in targets:
          missing = True
      if not missing:
        filtered_groupings.append(grouping)
  
  if not targets:
    filtered_groupings = groupings
  
  filtered_groupings = list(set(filtered_groupings))
  filtered_groupings.sort()
  return filtered_groupings

class Grouping:
  def __init__(self, groups):
    self.groups = sorted(groups)
    self.all_in = all(group.valid for group in groups)
    self.valid_groups = [group for group in self.groups if group.valid]
    self.invalid_groups = [group for group in self.groups if not group.valid]

  def __lt__(self, grouping):
    if self.all_in == grouping.all_in:
      return len(self.valid_groups) < len(grouping.valid_groups)
    else:
      return self.all_in
  
  def __eq__(self, grouping):
    return self.groups == grouping.groups and self.all_in == grouping.all_in

  def __hash__(self):
    return hash((tuple(self.groups), self.all_in))

  def __str__(self):
    roots = [group.root for group in self.valid_groups]
    return '{roots},  Valid: {valid},  Invalid: {invalid}'.format(roots=roots, valid=self.valid_groups, invalid=self.invalid_groups)

  def __repr__(self):
    return str(self)

class Group:
  def __init__(self, digits):
    self.members = sorted(list(digits))
    self.root = digital_root(self.members)
    self.valid = 3 <= len(self.members) <= 5

  def __lt__(self, group):
    if self.valid == group.valid:
      if self.root < group.root:
        return True
      elif self.root == group.root:
        return int(''.join(map(str, self.members))) < int(''.join(map(str, group.members)))
      else:
        return False
    else:
       return self.valid

  def __eq__(self, group):
    return self.valid == group.valid and self.root == group.root and self.members == group.members

  def __hash__(self):
    return hash((self.valid, self.root, tuple(self.members)))

  def __str__(self):
    return 'R: {root}, G: {group}.'.format(root=self.root, group=self.members)

  def __repr__(self):
    return str(self)

def list_sub(list1, list2):
  return [elem for elem in list1 if elem not in list2]

def test():
  print('Testing digital_root, 9,3,9')
  print(digital_root(numbers))
  print(digital_root([1,2]))
  print(digital_root(numbers[:-1]))

  print('Testing list_sub, [1], [1,2,3], [3,2,1]')
  print(list_sub([1,2], [2]))
  print(list_sub([1,2,3,4], [4,5,6,7]))
  print(list_sub([3,2,4,1,4,5], [4,5]))


if __name__ == '__main__':
  groupings = filter_splits([2, 4, 5, 7, 8],
                            targets=([8, 9]),
                            strict=True,
                            only_valid=False)
  for grouping in groupings:
    print(grouping)
  print(len(groupings))

