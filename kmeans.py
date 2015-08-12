from statistics import mean

data = {6, 15, 20, 24, 30, 42, 45}
centroids = [15, 40]
prev_centroids = []

while prev_centroids != centroids:
  partitions = [set(), set()]
  for datum in data:
    if abs(datum - centroids[0]) < abs(datum - centroids[1]):
      partitions[0].add(datum)
    else:
      partitions[1].add(datum)

  prev_centroids = centroids
  centroids[0] = mean(partitions[0])
  centroids[1] = mean(partitions[1])

print(partitions)
print(centroids)
