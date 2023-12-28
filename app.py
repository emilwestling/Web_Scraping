import seaborn as sns
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import nltk
from collections import Counter

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form["url"]
        text = fetch_text_from_url(url)
        top_words = analyze_text(text)
        # chart_filename = create_bar_chart(top_words)
        return render_template("index.html", top_words=top_words)
    return render_template("index.html")


def fetch_text_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        text = response.text
        return text
    except requests.exceptions.RequestException as e:
        return f"Error fetching content from URL: {str(e)}"


def analyze_text(text):
    html_soup = BeautifulSoup(text, 'html.parser')
    moby_text = html_soup.get_text()

    tokenizer = nltk.tokenize.RegexpTokenizer('\w+')
    tokens = tokenizer.tokenize(moby_text)
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()

    stops = nltk.corpus.stopwords.words('english')
    tokens_no_stop = []
    for i in range(len(tokens)):
        if tokens[i] not in stops:
            tokens_no_stop.append(tokens[i])

    counter = Counter(tokens_no_stop)
    top_words = counter.most_common(10)
    return top_words


if __name__ == "__main__":
    app.run(debug=True)
