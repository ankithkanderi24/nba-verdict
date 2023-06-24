from flask import Flask, render_template, request
from validateNames import *
from comparison import *

app = Flask(__name__)

@app.route('/', methods = ["GET", "POST"])
def home():
    return render_template('home.html')

@app.route('/comparison_page', methods = ["GET", "POST"])
def comparisonPage():
    p1name = request.form['p1name']
    p2name = request.form['p2name']

    validatedName = validateNames(p1name, p2name)
    if (validatedName != "Good"):
        return render_template('home.html', hiddenText = validatedName)
    else:
        dataP1 = getStats(p1name)
        dataP2 = getStats(p2name)
        return render_template('comparison.html', player1Data = dataP1, player2Data = dataP2, player1Name = p1name, player2Name = p2name)



if __name__ == '__main__':
   app.run(debug=True)