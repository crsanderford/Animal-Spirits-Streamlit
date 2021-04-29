# Animal-Spirits-Streamlit

A bitcoin sentiment analysis dashboard using Streamlit. Uses a linear support vector machine trained on the 2000 most correlated words in the tweet dataset.

Deployed to: [https://animal-spirits-crsanderford.herokuapp.com/](https://animal-spirits-crsanderford.herokuapp.com/)

# Running locally

Clone the repo:

```git clone <URL>```

In the project directory, create a .env file with the following environment variables (you will need keys to the Twitter API):

```
DATABASE_URL=<URL>

TWITTER_CONSUMER_KEY=<KEY>

TWITTER_CONSUMER_SECRET=<KEY>

TWITTER_ACCESS_TOKEN=<KEY>

TWITTER_ACCESS_TOKEN_SECRET=<KEY>
```

Create a pipenv environment and install the required dependencies with:

```
pipenv shell
pipenv install
```

Start the dashboard with the following command:
```
streamlit run app.py
```
