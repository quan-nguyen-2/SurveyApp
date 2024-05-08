from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)

survey = satisfaction_survey
title = survey.title

@app.route('/')
def start():  
    instructions = survey.instructions
    return render_template('start.html', title=title, instructions=instructions)

@app.route('/questions/<i>')
def question(i):
    i = int(i)        
    question = survey.questions[i].question   
    choices = survey.questions[i].choices 
    responses = session['responses']
    if i != len(responses):
        flash('Invalid Question ID')
        return redirect(f'/questions/{len(responses)}')
    else:    
        return render_template('questions.html', i=i, title=title, question=question, choices=choices)

@app.route('/answer', methods=["POST"])
def answer():
    choice = request.form['choice']
    responses = session['responses']
    responses.append(choice)
    session['responses'] = responses
    i = len(responses)
    if i == len(survey.questions):
        return redirect('/thanks')
    else:
        return redirect(f'/questions/{i}')

@app.route('/thanks')
def thanks():
    return render_template('thanks.html', title=title)

@app.route('/session', methods=['POST'])
def start_session():
    session['responses'] = []
    responses = session['responses']
    session['i'] = len(responses)
    return redirect(f'/questions/{len(responses)}')