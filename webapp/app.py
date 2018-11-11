from flask import Flask, render_template, request, jsonify, abort
from sklearn import svm

from webapp.predictor import Predictor


app = Flask(__name__)

predictor = Predictor(svm.LinearSVC(), '../models/demo_model_tfidf1.joblib')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/get_sentence_result', methods=['POST'])
def get_sentence_result():
    text = request.form['text']
    if text:
        bullying = predictor.predict(text)
    else:
        abort(500)
    return jsonify(result=text.upper(), bullying=bool(bullying))


if __name__ == '__main__':
    app.run(debug=True)
