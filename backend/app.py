from flask import Flask
from flask import jsonify
import utils.scraper as scraper
import utils.analyzer as analyzer
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/analyze/<ticker>')
def analyze(ticker):
    try:
        all_posts = scraper.get_all_discussions(ticker)
        analysis = analyzer.get_overall_sentiment(all_posts)
        percentage = analyzer.get_percentage_sentiment(analysis)
        return f'Analyzing {ticker}: {analysis}. All texts: {all_posts} \n\n\n\nPercentages: {percentage[0]}% positive, {percentage[1]}% negative.'
    except Exception as e:
        return str(e)
    
@app.route("/analyze/percent/<ticker>")
def analyze_percent(ticker):
    all_posts = scraper.get_all_discussions(ticker)
    analysis = analyzer.get_overall_sentiment(all_posts)
    percentage = analyzer.get_percentage_sentiment(analysis)
    response = jsonify({"positive":percentage[0],
                        "negative":percentage[1],
                        "total":percentage[2]})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(debug=True)