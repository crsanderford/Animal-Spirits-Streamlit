import streamlit as st
import psycopg2

import pandas as pd
import altair as alt

import animal_spirits_imports as asm
from sqlalchemy import func
from animal_spirits_imports.twitter import Tweet


def main():

    asm.twitter.insert_tweets(7000)
    asm.twitter.delete_tweets()

    session = asm.twitter.Session()

    indicator = session.query(func.avg(Tweet.sentiment)).scalar()
    negative = session.query(func.count(Tweet.sentiment)).filter(Tweet.sentiment == -1).scalar()
    neutral = session.query(func.count(Tweet.sentiment)).filter(Tweet.sentiment == 0).scalar()
    positive = session.query(func.count(Tweet.sentiment)).filter(Tweet.sentiment == 1).scalar()

    session.commit()
    session.close()

    sidebutton = st.sidebar.button(label='refresh tweets?')

    if sidebutton:
        asm.twitter.delete_tweets()
        asm.twitter.insert_tweets(1000)
        asm.twitter.delete_tweets()

        indicator = session.query(func.avg(Tweet.sentiment)).scalar()
        negative = session.query(func.count(Tweet.sentiment)).filter(Tweet.sentiment == -1).scalar()
        neutral = session.query(func.count(Tweet.sentiment)).filter(Tweet.sentiment == 0).scalar()
        positive = session.query(func.count(Tweet.sentiment)).filter(Tweet.sentiment == 1).scalar()

        session.commit()
        session.close()

    explanation = st.sidebar.markdown(body="""a *very* simple indicator for sentiment about bitcoin on Twitter.
                                              tweets are scored using sklearn's CountVectorizer and LinearSVC,
                                              limited to the 2000 most correlated 1-grams as determined by SelectKBest.
                                              the index is just an average of the sentiment scores stored in 
                                              the database - it is not normalized based on historical data.""")

    explanation2 = st.sidebar.markdown(body="""the model scores well in cross-validation, but not so well when applied
                                               to new tweets - the dataset used spanned the time of about one day in 
                                               March 2018, during a period of decline. 1-grams that were predictive then 
                                               may be less so now.""")

    explanation3 = st.sidebar.markdown(body="""more of my work located [here.](http://www.crsanderford.github.io)""")


    st.title('Animal Spirits')

    st.write(f'Sentiment Index: {round(indicator, 2)}')

    sentiments = pd.DataFrame(['negative','neutral','positive'],[negative,neutral,positive]).reset_index()
    sentiments.columns = ['counts','sentiment']

    sentiment_chart = alt.Chart(
        sentiments,
        title='Bitcoin Sentiment'
    ).mark_bar(size=50).encode(
        x=alt.X('counts', title = 'frequency', sort = None),
        y=alt.Y(
            'sentiment',
            title = 'sentiment',
            sort=['positive', 'neutral', 'negative']
        ),
        color=alt.Color('counts', title=None, scale=alt.Scale(scheme="brownbluegreen")),
        tooltip=[
            alt.Tooltip('counts', title='frequency'),
        ]
    ).configure_mark(opacity=0.8).properties(width=700, height=400)

    st.write(sentiment_chart)

if __name__ == "__main__":
    main()