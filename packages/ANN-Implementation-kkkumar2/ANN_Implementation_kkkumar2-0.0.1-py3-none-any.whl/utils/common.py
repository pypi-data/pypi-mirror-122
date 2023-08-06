import yaml

def read_config(filename):
    with open(filename, 'r') as config_file:
        content = yaml.safe_load(config_file)
        return content