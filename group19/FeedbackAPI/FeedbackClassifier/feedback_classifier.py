"""
Feedback Classifier for the FeedbackAPI app.

Run this script to train a classifier on the feedback data and save it to disk.
"""
import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

# Load the training data as a pandas DataFrame
data_frame = pd.read_csv('feedback_training_data.csv')

# Create a CountVectorizer object
vectorizer = CountVectorizer()

# Transform the feedback data into a matrix of token counts
X = vectorizer.fit_transform(data_frame['Feedback'])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, data_frame['Category'], test_size=0.2, random_state=42)

# Create a Multinomial Naive Bayes classifier
clf = MultinomialNB()

# Train the classifier on the training data
clf.fit(X_train, y_train)

# Make predictions on the test data
y_pred = clf.predict(X_test)

# Print report
print(classification_report(y_test, y_pred, zero_division=1))

# Save the classifier and vectorizer to disk
joblib.dump(clf, 'feedback_classifier.pkl')
joblib.dump(vectorizer, 'feedback_vectorizer.pkl')
