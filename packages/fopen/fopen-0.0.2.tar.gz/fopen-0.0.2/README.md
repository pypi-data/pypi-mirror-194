## [github](https://github.com/chemtrails/filetools)
### Simple read/write wrapper

`pip install fopen`

**any format**
```
from fopen import Fopen

f = Fopen('file.txt')
f.content
# line 1
  line 2

for line in f.read_lines():
    print(line)
    break
# line 1

f.append_line('line 3')
f.clear() # empties file
```

**JSON lines**
```
f = Fopen('file.jsonl')
f.content
# {"a": 1, "b": 2}
  {"a": 2, "b": 3}

for line in f.read_lines():
    print(line['a'])
# 1
  2

dict = {'a': 3, 'b': 4}
f.append_line(dict)
f.content
# {"a": 1, "b": 2}
  {"a": 2, "b": 3}
  {"a": 3, "b": 4}

f.to_json_array()
# [{"a": 1, "b": 2}, {"a": 2, "b": 3}, {"a": 3, "b": 4}]
```

**csv**
```
f = Fopen('file.csv')
f.content
# a,b,c
  d,e,f

for line in f.read_lines():
    print(line[1])
# b
  e

l = ['g', 'h', 'i']
f.append_line(l)
f.content
# a,b,c
  d,e,f
  g,h,i
```