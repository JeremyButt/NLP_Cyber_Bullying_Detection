from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/get_sentence_result', methods=['POST'])
def get_sentence_result():
    text = request.form['text']
    return jsonify(result=text.upper(), bullying=False)


if __name__ == '__main__':
    app.run()
