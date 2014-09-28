import os.path


def loadProperties(propertyFile):
    if not os.path.isfile(propertyFile):
        raise Exception('%s does not exist' % propertyFile)
    
    properties = {}
    with open(propertyFile, 'r') as f:
        for line in f:
            line = line.rstrip()
            if '=' not in line: continue
            if line.startswith('#'): continue
            k, v = line.split('=', 1)
            properties[k] = v
    return properties
