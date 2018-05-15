import yaml

with open('calib.yaml') as doc:
    load = yaml.load(doc)
    yaml.dump(load, default_flow_style=False)
