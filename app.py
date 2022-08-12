from surveys import surveys
from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension

responses = []
satisfaction_survey = surveys['satisfaction']

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def home():

    return render_template('home.html', survey=satisfaction_survey)

@app.route('/questions/<int:num>')
def question(num):

    questions = satisfaction_survey.questions
    resplen = len(responses)

    if num != resplen:
        flash("WHOOPS!!! You tried going to a question out of order or that question doesn't exist.")
        return redirect('/questions/'+str(resplen))
    else:
        try:
            question = questions[resplen]
            return render_template('question.html', question=question, survey=satisfaction_survey, qnum=num)
        except IndexError:
            return "That concludes the survey. THANK YOU!!!"

@app.route('/answer', methods=['POST'])
def post_answer():
    responses.append(request.form['answer'])
    qnum = request.form['qnum']
    return redirect('/questions/' + qnum)