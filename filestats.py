import os
import sys

path = sys.argv[-1]
sizes = {}

for dirpath, dirnames, filenames in os.walk(path):
  for filename in filenames:
    file_ = os.path.join(dirpath, filename)
    name, ext = os.path.splitext(filename)
    ext = ext.lower()
    size = os.path.getsize(file_)
    if ext in sizes:
      sizes[ext].append(size)
    else:
      sizes[ext] = [size]

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

for ext, size in sorted(sizes.items(), key=lambda x:sum(x[1]), reverse=True):
  print('{}: {} {}'.format(ext, sizeof_fmt(sum(size)), len(size)))

