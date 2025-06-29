from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pandas as pd  # ✅ <--- This line is necessary

app = Flask(__name__)

# Load dataset
df = pd.read_csv("sms.tsv", sep='\t', header=None, names=["label", "text"])
df['label'] = df['label'].str.lower()

# Vectorize using TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['text'])
y = df['label']

# Train Logistic Regression
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = ""
    if request.method == 'POST':
        email = request.form['email']
        email_vector = vectorizer.transform([email])
        result = model.predict(email_vector)
        prediction = "This is SPAM!" if result[0] == 'spam' else "This is NOT spam."
    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
