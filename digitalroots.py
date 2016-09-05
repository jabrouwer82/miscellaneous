#!/bin/python2.7
"""This was made for fun to accompany my playthrough of the DS/computer game "999" wherein
character are assigned digits and forced to split into groups of 3, 4, or 5 members where each
group must have a digital root matching the number marked on doors to enter certain puzzle rooms.

This module contain methods for calculating digital roots, finding combinatoric groupings of
players, and filtering those groups based on door targets.

It also contains python generators, classes with operator overloading, list comprehensions,
recursion methods, .

For more information on digital roots, see: https://en.wikipedia.org/wiki/Digital_root."""

import itertools
import math

def digital_root(nums):
  """Calculates the digital root of the given list of numbers."""
  root = sum(nums)

  if root > 0:
    num_digits = math.log10(root) + 1
  else:
    # If the given number is 0, then the root is 0.
    return 0

  if num_digits >= 2:
    # Digital roots must be a single digit, so we must recurse.
    new_nums = list(digits(root))
    return digital_root(new_nums)
  else:
    return root
  
def digits(num):
  """A generator that yields the digits of the given integer in reverse order."""
  while num > 0 and math.log10(num) >= 0:
    num, digit = divmod(num, 10)
    yield digit

def all_possible_groupings(digits, groups_so_far=(), groupings=()):
  """Returns a list of every possible Grouping of Groups with 5 or fewer members such that every
  digit is used exactly once per Grouping.
  
  For example:
  When given less than 3 digits, a single Grouping containing a single invalid Group is returned..
  When given exactly 3 digits, only a single valid Group is returned.
  When given [1, 2, 3, 4], the following 5 gropuings are returned:
  ([1, 2, 3], [4]), ([1, 2, 4], [3]), ([1, 3, 4], [2]), ([2, 3, 4], [1]), ([1, 2, 3, 4]).
  Etc.
  """
  if not groupings:
    groupings = []
  # Determines every possible combination of 3, 4, or 5 digits from the given digits.
  combinations = [itertools.combinations(digits, length) for length in range(3, 6)]
  # Flatten the list of lists.
  combinations = [elem for combination_list in combinations for elem in combination_list]
  for combination in combinations:
    unused_digits = list(set(digits) - set(combination))
    groups = list(groups_so_far)
    groups.append(Group(combination))
    # Recurse to see if there are more Groups that can be made from the unused digits.
    groupings = all_possible_groupings(unused_digits, groups_so_far=groups, groupings=groupings)
  if not combinations:
    # No combinations means that there are not enough digits left to make a valid Group.
    groups = list(groups_so_far)
    if digits:
      # Throw the last couple digits into an inbalid Group.
      groups.append(Group(digits))
    # No more Groups can be mdae from this set of combinations, so we create a Grouping and return.
    groupings.append(Grouping(groups))
  return groupings
  
def filter_groupings(digits, target_roots=(), strict=False, only_valid=False):
  """Creates all possible groupings for the given digits, then returns those which contain groups
  whose digital roots match the target roots.

  If strict is true, then the grouping's groups must share at least one root with the target roots.
  If strict is false, the the grouping's groups' roots must be a superset of the target roots.

  If only_valid is true, then the grouping must contain only valid groups, and if false groupings
  can contain extra invalid groups.
  """
  groupings = all_possible_groupings(digits)
  if only_valid:
    # Removes groupings containing invalid groups.
    groupings = [grouping for grouping in groupings if len(grouping.invalid_groups) == 0]
  filtered_groupings = []
  
  if target_roots and not strict:
    for grouping in groupings:
      group_roots = [group.root for group in grouping.valid_groups]
      if len(set(group_roots) & set(target_roots)) >= 1:
        # If the set interesction of the group roots and the target roots contains any elements
        # then we have a non-strict match.
        filtered_groupings.append(grouping)

  if target_roots and strict:
    for grouping in groupings:
      group_roots = [group.root for group in grouping.valid_groups]
      if set(group_roots) >= set(target_roots):
        # If the group roots is a superset of the target roots the we have a strict match.
        filtered_groupings.append(grouping)
  
  if not target_roots:
    # Without targets, everything is valid.
    filtered_groupings = groupings
  
  filtered_groupings = list(set(filtered_groupings))
  filtered_groupings.sort()
  return filtered_groupings

class Grouping:
  """Represents a list of 999 player groups.
  
  Groupings are sorted by the presence of all digits then by its number of valid groups."""
  def __init__(self, groups):
    self.groups = sorted(groups)
    self.all_valid = all(group.valid for group in groups)
    self.valid_groups = [group for group in self.groups if group.valid]
    self.invalid_groups = [group for group in self.groups if not group.valid]

  def __lt__(self, grouping):
    if self.all_valid == grouping.all_valid:
      return len(self.valid_groups) < len(grouping.valid_groups)
    else:
      return self.all_valid
  
  def __eq__(self, grouping):
    return (self.groups == grouping.groups
          and self.all_valid == grouping.all_valid)

  def __hash__(self):
    return hash((tuple(self.groups), self.all_valid))

  def __str__(self):
    roots = [group.root for group in self.valid_groups]
    return ('Roots: {roots},  Valid Groups: {valid},  Invalid Groups: {invalid}'
          .format(roots=roots, valid=self.valid_groups, invalid=self.invalid_groups))

  def __repr__(self):
    return str(self)

class Group:
  """Represents a group of 999 players.
  
  Groups each have a digital root determined by the players assigned numbers.
  To be valid group, there can only be 3, 4, or 5 players present.
  
  Groups are sorted by validity, and then by digital root, then by player digit concatenation"""
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
    return 'Root: {root}, Members: {members}'.format(root=self.root, members=self.members)

  def __repr__(self):
    return str(self)

if __name__ == '__main__':
  players = [1, 2, 4, 5, 7, 8, 9]
  targets = [8, 9]
  print "If we have the following players: " + str(players)
  print "And they must split into groups to matching the following roots: " + str(targets)
  print "Then thier options for splitting are the following:"
  print
  print "If they need a group for each target:"
  groupings = filter_groupings(players, target_roots=targets, strict=True, only_valid=False)
  print "They have " + str(len(groupings)) + " options:"
  for grouping in groupings:
    print grouping
  print
  print "If every player needs to be in a group:"
  groupings = filter_groupings(players, target_roots=targets, strict=False, only_valid=True)
  print "They have " + str(len(groupings)) + " options:"
  for grouping in groupings:
    print grouping

