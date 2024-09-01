import pandas as pd
import numpy as np
from textblob import TextBlob
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Daten laden
data = pd.read_csv("stock_data.csv")
tweets = pd.read_csv("tweets.csv")

# Sentiment-Analyse
def sentiment(text):
    analysis = TextBlob(text)
    return analysis.sentiment.polarity

tweets['sentiment'] = tweets['text'].apply(sentiment)

# Feature-Engineering
features = ['close', 'volume', 'sentiment']
target = 'target'  # z.B. ob der Kurs am nächsten Tag steigt oder fällt

# Modell trainieren
X_train, X_test, y_train, y_test = train_test_split(data[features], data[target], test_size=0.2)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Vorhersage
predictions = model.predict(X_test)
