import streamlit as st
import psycopg2

from time import sleep
from datetime import datetime

import pandas as pd
import altair as alt

import animal_spirits_imports as asm
from sqlalchemy import func
from animal_spirits_imports.twitter import Tweet, IndicatorRecord


def main():

    asm.twitter.insert_tweets(1000)
    asm.twitter.delete_tweets()

    st.title('Animal Spirits')

    

    explanation = st.sidebar.markdown(body="""*“Most, probably, of our decisions to do something positive, 
                                               the full consequences of which will be drawn out over many days to come, 
                                               can only be taken as the result of animal spirits – a spontaneous urge 
                                               to action rather than inaction, and not as the outcome of a weighted 
                                               average of quantitative benefits multiplied by quantitative probabilities.”*""")

    explanation1 = st.sidebar.markdown(body="""a *very* simple indicator for sentiment about bitcoin on Twitter.
                                            tweets are scored using sklearn's CountVectorizer and LinearSVC,
                                            limited to the 2000 most correlated 1-grams as determined by SelectKBest.
                                            the index is just an average of the sentiment scores stored in 
                                            the database - it is not normalized based on historical data.""")

    explanation2 = st.sidebar.markdown(body="""the model scores well in cross-validation, but not so well when applied
                                            to new tweets - the dataset used spanned the time of about one day in 
                                            March 2018, during a period of decline. 1-grams that were predictive then 
                                            may be less so now.""")

    explanation3 = st.sidebar.markdown(body="""more of my work located [here.](http://www.crsanderford.github.io)
                                               read more about the model itself [here.](https://crsanderford.github.io/posts/2019/10/23/animal-spirits-post.html)""")

    sentiment_index = st.empty()

    sentiment_chart = st.empty()

    indicator_chart = st.empty()

    while(True):
        # database logic stuff
        asm.twitter.delete_tweets()
        asm.twitter.insert_tweets(1000)
        asm.twitter.delete_tweets()

        session = asm.twitter.Session()

        current_indicator = session.query(func.avg(Tweet.sentiment)).scalar()
        negative = session.query(func.count(Tweet.sentiment)).filter(Tweet.sentiment == -1).scalar()
        neutral = session.query(func.count(Tweet.sentiment)).filter(Tweet.sentiment == 0).scalar()
        positive = session.query(func.count(Tweet.sentiment)).filter(Tweet.sentiment == 1).scalar()

        asm.twitter.delete_indicator_records()
        asm.twitter.insert_indicator_record(round(current_indicator, 2), datetime.now())
        asm.twitter.delete_indicator_records()

        indicator_date_query = session.query(IndicatorRecord.time_generated)
        indicator_dates = [r[0] for r in indicator_date_query]

        indicator_value_query = session.query(IndicatorRecord.indicator_value)
        indicator_values = [r[0] for r in indicator_value_query]

        session.commit()
        session.close()
        

        # update the current sentiment indicator value
        sentiment_index.text(f'sentiment index: {round(current_indicator, 2)}')


        # use the sentiments pulled from the DB to construct a dataframe and chart
        sentiments = pd.DataFrame(['negative','neutral','positive'],[negative,neutral,positive]).reset_index()
        sentiments.columns = ['counts','sentiment']

        sentiment_chart_to_serve = alt.Chart(
            sentiments,
            title='bitcoin sentiment'
        ).mark_bar(size=50).encode(
            x=alt.X('counts', title = 'frequency', sort = None),
            y=alt.Y(
                'sentiment',
                title = 'sentiment',
                sort=['positive', 'neutral', 'negative']
            ),
            color=alt.Color('counts', title=None, scale=alt.Scale(scheme="goldorange")),
            tooltip=[
                alt.Tooltip('counts', title='frequency'),
            ]
        ).configure_mark(opacity=0.8).properties(width=700, height=400)

        sentiment_chart.altair_chart(sentiment_chart_to_serve)

        historical_indicators = pd.DataFrame(indicator_dates,indicator_values).reset_index()
        historical_indicators.columns = ['values','dates']

        indicator_chart_to_serve = alt.Chart(
            historical_indicators,
            title='historical index values'
        ).mark_bar().encode(
            x=alt.X('dates', title = 'time'),
            y=alt.Y(
                'values',
                title = 'index value',
            ),
            color=alt.Color('values', title=None, scale=alt.Scale(scheme="goldorange")),
            tooltip=[
                alt.Tooltip('values', title='index value'),
                alt.Tooltip('dates', title='time'),
            ]
        ).configure_mark(opacity=0.8).properties(width=700, height=400)

        indicator_chart.altair_chart(indicator_chart_to_serve)

        sleep(3600)

        print('...looping...')



if __name__ == "__main__":
    main()