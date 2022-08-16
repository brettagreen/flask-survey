from surveys import surveys
from flask import Flask, render_template, request, redirect, flash, session, make_response
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "bush-did-911"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def choose_survey():
    return render_template('choice.html', surveys=surveys)


@app.route('/start', methods=['POST'])
def start():
    survey = surveys[request.form['survey']]
    completed = request.cookies.get(survey.title, None)
    if completed:
        flash(f"y'all already done did the {survey.title} survey...choose another one!")
        return redirect('/')
    else:
        session['title'] = survey.title
        return render_template('home.html', survey=survey)


@app.route('/initiate', methods=['POST'])
def init():
    session['responses'] = []
    session['comments'] = []

    return redirect('/questions/0')


@app.route('/questions/<int:num>')
def question(num):

    survey = surveys['satisfaction'] if session['title'] == "Customer Satisfaction Survey" else surveys['personality']
    questions = survey.questions
    resplen = len(session['responses'])

    if num != resplen:
        flash("WHOOPS!!! You tried going to a question out of order or that question doesn't exist.")
        return redirect('/questions/'+str(resplen))
    else:
        try:
            question = questions[resplen]
            return render_template('question.html', question=question, survey=survey, qnum=num)
        except IndexError:
            html = render_template('complete.html', questions=questions, responses=session['responses'])
            response = make_response(html)
            response.set_cookie(survey.title, 'complete')
            return response

@app.route('/answer', methods=['POST'])
def post_answer():
    qnum = request.form['qnum']
    try:
        ans = request.form['answer']
        responses = session['responses']
        comment = request.form.get('comment', None)
        if comment:
            comments = session['comments']
            comments.append(f'comment on survey question {qnum}: {comment}')
            session['comments'] = comments
        responses.append(ans)
        session['responses'] = responses
        return redirect('/questions/' + qnum)
    except KeyError:
        flash('you must choose an answer')
        return redirect('/questions/' + str(int(qnum) - 1))