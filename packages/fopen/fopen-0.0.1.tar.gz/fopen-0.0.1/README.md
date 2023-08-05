Simple read/write wrapper for several file formats

`from fopen import Fopen`

init parameters
```
path:Path
delimiter:str = ','
enc:str = 'utf-8'
```

**JSON lines**
```
f = Fopen("file.jsonl")

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

f.clear() # empties file
```

**csv**
```
f = Fopen("file.csv")

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

f.clear()
```

**txt**
```
f = Fopen("file.txt")

f.content
# text 1
  text 2

for line in f.read_lines():
    print(line)

# text 1
  text 2

f.append_line("text 3")

f.content
# text 1
  text 2
  text 3

f.clear()
```
