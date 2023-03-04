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



#this function takes in a list of comments and outputs a corresponding list of sentiment scores ranging from -1 to 1
def sentScore(comment):

    #initalize an empty array for the scores
    score = 0

    #initalize the model
    sid = SentimentIntensityAnalyzer()

    
   
        #a dictionary 
    s =  sid.polarity_scores(comment)
        
    for key, value in s.items():
        if(key == 'compound'):
            score = value
        
        

    #OPTIONAL could use to return a tuple of the comments and the sentiment score to be put into a database 
    #comsAndScores = {}
    #for key in comments:
    #    for value in score:
    #        comsAndScores[key] = value
    #        score.remove(value)
    #        break

    #todo figure out average sent score for a whole video
    


    #print(score)
    return score


#example list of comments
comments = ["Hello my name is Sam.", "i hate pizza", "I love cookies"]



def aveSentScore(s):
    total = 0
    for comment in comments:
        total = total + sentScore(comment)
    return(total/len(s))



    