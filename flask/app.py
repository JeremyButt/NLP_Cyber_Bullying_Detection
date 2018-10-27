from flask import Flask, render_template, request, jsonify, abort
from predict import predict

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/get_sentence_result', methods=['POST'])
def get_sentence_result():
    text = request.form['text']
    if text:
        bullying = predict(text)
    else:
        abort(500)
    return jsonify(result=text.upper(), bullying=bullying)


if __name__ == '__main__':
    app.run(debug=True)
