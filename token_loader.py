def loadToken(path):
    with open(path) as file:
        token = file.readline()
        return token