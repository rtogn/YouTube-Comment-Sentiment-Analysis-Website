from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('vader_lexicon')


def getComments():
    #example list of comments
    comments = ["Hello my name is Sam.", "i hate pizza", "I love cookies"]

    #initalize an empty array for the scores
    scores = []


    #initalize the model
    sid = SentimentIntensityAnalyzer()

    for comment in comments:
        scores.append(sid.polarity_scores(comment))
        


    #comsAndScores = {}
    #for key in comments:
    #    for value in scores:
    #        comsAndScores[key] = value
    #        scores.remove(value)
    #        break

    #returns a tuple of the comments and the sentiment score to be put into a database 
    print(scores)
    return scores
getComments()



    