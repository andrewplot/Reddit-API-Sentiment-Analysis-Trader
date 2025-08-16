#Finds latest post from user-inputted subreddit with over 20 comments, prints scatter plot, box and whisker plot, and a broken histogram/kde bell curve

import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px
import plotly.graph_objects as go

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
        if post.num_comments > 20:
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
    return(score)

def plotScores(scoresList):
    compounds = [score['compound'] for score in scoresList]
    positives = [score['pos'] for score in scoresList]
    negatives = [score['neg'] for score in scoresList]
    neutrals = [score['neu'] for score in scoresList]
    
    # Creating the scatter plot
    scatter_fig = px.scatter(x=positives, y=negatives, color=compounds,
                             labels={'x': 'Positive', 'y': 'Negative', 'color': 'Compound'},
                             title='Sentiment Analysis Scatter Plot')
    scatter_fig.show()

    # Creating the box and whisker plot for compound scores
    box_fig = px.box(compounds, title='Box and Whisker Plot of Compound Scores')
    box_fig.update_layout(xaxis_title='Compound Score', yaxis_title='Value')
    box_fig.show()

    # Creating the smoothed bell curve (KDE) for compound scores
    kde_fig = go.Figure()
    kde_fig.add_trace(go.Histogram(x=compounds, histnorm='density', name='Histogram'))
    kde_fig.add_trace(go.Scatter(x=compounds, y=px.histogram(compounds, histnorm='density').data[0].y,
                                 mode='lines', name='KDE'))
    kde_fig.update_layout(title='Smoothed Bell Curve of Compound Scores',
                          xaxis_title='Compound Score', yaxis_title='Density')
    kde_fig.show()

if __name__ == "__main__":
    subredditName = input("Enter the subreddit name: ")
    analyzer = SentimentIntensityAnalyzer()
    scoresList = getCommentsFromPostWithOver50Comments(subredditName)
    if scoresList:
        plotScores(scoresList)