from flask import Flask, render_template, jsonify, request
from .speech import Speech

app = Flask(__name__)
bot = Speech()
query = ''


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/listen')
def listen():
    query = bot.talk_in_mic()
    print(query)
    if bot.check_voice(query):
        return jsonify({"query": query.text})


@app.route('/answer/<query>', methods=["POST"])
def answer(query):
    temp = float(request.form['temperature'])
    print(temp)
    answer_txt = bot.get_textual_answers(query, temp=temp)
    print(answer_txt)
    return jsonify({"answer": answer_txt, "query": query})


@app.route('/speech/<answer>')
def speech(answer):
    language = request.args.get("language")
    msg = bot.get_vocal_answers(answer, language=language)
    return jsonify(msg)
