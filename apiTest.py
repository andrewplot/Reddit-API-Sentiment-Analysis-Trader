import praw
from praw.exceptions import APIException
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy.stats import gaussian_kde
#add api call limit error exception
#retrain vader
#take inverse from comments with negative upvotes 

# Create a Reddit instance
reddit = praw.Reddit(
    client_id="TpYpEuvSGqjOogwld6GF3A",
    client_secret="BbmcT9t0apw2nmARIyPHAq7_pSv1hQ",
    user_agent="Sentiment Analysis Research by /u/Andrewplotplot"
)

def getCommentsFromPostWithOver50Comments(subredditName):
    subreddit = reddit.subreddit(subredditName)  # 1st API call

    # Find the most recent post with over 50 comments
    for post in subreddit.new(limit=100):  # No additional API calls, still part of the first one
        if post.num_comments > 80:
            latestPost = post
            break
    else:
        print("No recent post with over 50 comments found.")
        return []

    print(f"Title: {latestPost.title}\n")  # Prints title of the post
    print("Comments:\n")

    latestPost.comments.replace_more(limit=0)  # 2nd API call to expand comments
    scoreList = []  # List of scores

    for comment in latestPost.comments.list():  # No additional API calls
        print(f"\n{comment.body}")  # Prints comment
        score = performSentiment(comment.body)
        print(score)
        scoreList.append(score)

    return scoreList

def performSentiment(text):
    score = analyzer.polarity_scores(text)
    return score

def plotScores(scoresList):
    #Extract values from dictionary
    compounds = [score['compound'] for score in scoresList]
    positives = [score['pos'] for score in scoresList]
    negatives = [score['neg'] for score in scoresList]
    neutrals = [score['neu'] for score in scoresList]
    
    #SCATTER PLOT
    scatter_fig = px.scatter(x=positives, y=negatives, color=compounds,
                             labels={'x': 'Positive', 'y': 'Negative', 'color': 'Compound'},
                             title='Sentiment Analysis Scatter Plot')
    scatter_fig.update_xaxes(range=[0, 1]) #sets axis scales
    scatter_fig.update_yaxes(range=[0, 1])
    scatter_fig.show()

    # # #BOX AND WHISKER
    box_fig = px.box(x=compounds, title='Box and Whisker Plot of Compound Scores')
    box_fig.update_layout(xaxis_title='Compound Score', yaxis_title='Value')
    box_fig.show()

    # #HISTOGRAM
    hist_fig = px.histogram(x=compounds, nbins=100, marginal='rug', title='Histogram with Kernel Density Estimator of Compound Scores')
    hist_fig.update_traces(opacity=0.75)

    # #KDE CALCULATION
    kde = gaussian_kde(compounds)
    x_vals = np.linspace(min(compounds), max(compounds), 1000)
    y_vals = kde(x_vals)
    
    # #ADDING KDE TO HISTOGRAM
    hist_fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name='KDE'))

    hist_fig.update_layout(xaxis_title='Compound Score', yaxis_title='Density')
    hist_fig.show()

if __name__ == "__main__":
    subredditName = input("Enter the subreddit name: ")
    analyzer = SentimentIntensityAnalyzer()
    scoresList = getCommentsFromPostWithOver50Comments(subredditName)
    if scoresList:
        plotScores(scoresList)
