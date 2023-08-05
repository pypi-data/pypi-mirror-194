
id=1;
data=[{'unique_id': 1, 'parent_id': 0, 'short_name': '', 'type': ' ', 'description': ' '}];
v=list(AppPyAMS.elements.values())
k=list(AppPyAMS.elements.keys())


id=id+1;
r=id;

data += [{'unique_id': id, 'parent_id': 1, 'short_name': 'Wire', 'type': ' ', 'description': ' '}]
for j in range(len(net)):
    id=id+1;
    data += [{'unique_id': id, 'parent_id': r, 'short_name':net[j]+'.V', 'type': 'wire', 'description': ''}]


for i in range(len(v)):
    signals=v[i].getSignals();
    params=v[i].getParamaters();
    id=id+1;
    r=id
    data += [{'unique_id': id, 'parent_id': 1, 'short_name': k[i], 'type': ' ', 'description': ' '}]
    for j in range(len(signals)):
          id=id+1;
          data += [{'unique_id': id, 'parent_id': r, 'short_name': signals[j].name, 'type': 'signal', 'description': signals[j].type, 'dir': signals[j].dir}]
    for j in range(len(params)):
          id=id+1;
          data += [{'unique_id': id, 'parent_id': r, 'short_name': params[j].name, 'type': 'paramater', 'description': ''}]


file = open(result, "w", encoding="utf-8")
file.write(str(data))
file.close();