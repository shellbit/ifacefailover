import pickle


def serialize(obj, filename):
    with open(filename, 'wb') as outputStream:
        pickle.dump(obj, outputStream, pickle.HIGHEST_PROTOCOL)

def deserialize(filename):
    with open(filename, 'rb') as inputStream:
        return pickle.load(inputStream)
