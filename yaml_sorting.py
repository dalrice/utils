from collections import OrderedDict
import yaml

def represent_ordereddict(dumper, data):
    value = []
    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)
        value.append((node_key, node_value))
    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)
yaml.add_representer(OrderedDict, represent_ordereddict)

with open("./filename", "r") as f:
    s = f.read()
    dct_obj = yaml.safe_load(s)
    obj = list(dct_obj.items())
    obj.sort()
    od = OrderedDict(obj)
    with open('./newfile', 'w') as abc:
        abc.write(yaml.dump(od, default_flow_style=False))

