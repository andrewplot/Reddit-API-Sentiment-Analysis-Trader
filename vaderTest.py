from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
angry_review = 'The food was disgusting. I am never coming back here again!!'
score = analyzer.polarity_scores(angry_review)
print(score)