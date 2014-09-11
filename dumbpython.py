def countURL(data):
    pass

def punctRatio(data):
    pass

def numberOfSensitiveWords(data):
    pass

def capitalizedWordCount(data):
    pass

def bagOfWords(data):
    pass

features = [countURL,
            punctRatio,
            numberOfSensitiveWords,
            capitalizedWordCount,
            bagOfWords,]

def process(data, output, features):
    for f in features:
        output[f.__name__] = f(data)
    return output
