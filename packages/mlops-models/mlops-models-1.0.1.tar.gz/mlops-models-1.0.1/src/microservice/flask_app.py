import flask

from src.mlops_models.sentiment import TweetSentiment

app = flask.Flask(__name__)

@app.route('/ping')
def ping():
    return 'pong'


@app.route('/sentiment/<text>')
def sentiment_analysis(text):
    model = TweetSentiment()
    return f"{model.predict(text)}"


@app.route('/', methods=['GET', 'POST'])
def sentiment_analysis_form():
    # Render HTML form
    if flask.request.method == 'GET':
        return flask.render_template('sentiment_form.html')

    elif flask.request.method == 'POST':
        # Get text from form
        text = flask.request.form['text']
        # Predict sentiment
        model = TweetSentiment()
        sentiment = model.predict(text)
        # Render HTML form with prediction
        return flask.render_template('sentiment_form.html', text=text, sentiment=sentiment)


if __name__ == '__main__':
    app.run(port=5000, debug=True)