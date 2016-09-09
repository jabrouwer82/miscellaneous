import itertools

size = 4
shape = [0] * size

vertices = list(itertools.product(*zip(shape, [1] * size)))

print(vertices)

