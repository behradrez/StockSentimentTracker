from textblob import TextBlob

def get_sentiment(text:str):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

def get_overall_sentiment(post_texts:list):
    positives = 0
    negatives = 0
    neutrals = 0

    for text in post_texts:
        try:
            sentiment = get_sentiment(text)
        except TypeError:
            continue
        if sentiment > 0:
            positives+=1
        elif sentiment < 0:
            negatives+=1
        else:
            neutrals+=1
    return [positives,negatives,neutrals]

def get_percentage_sentiment(analysis:list):
    total = analysis[0]+analysis[1]
    if total == 0:
        return [0,0,0]
    return [round((analysis[0]/total)*100,2),round((analysis[1]/total)*100,2), sum(analysis)]

    