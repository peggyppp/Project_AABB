import os, requests

from flask import Flask, session, render_template, request
from flask_session import Session
from random import randint


app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    session['target'] = []
    session['answer'] = []
    session['check'] = []

    # For non-duplicate number
    while len(session['target']) < 4:
        i = randint(0,9)
        if i not in session['target']:
            session['target'].append(i)

    # # For duplicatable number
    # for i in range(4):
    #     session['target'].append(randint(0,9))
    print('target=',session['target'])

    return render_template("index.html")

@app.route("/", methods=["POST"])
def check():

    answer_ls = []
    the_row_results = ["Guess", "Result"]
    answer = request.form.get("answer")
    message = ''
    check_result=" "

    print('ans type=', type(answer), answer, answer.isdigit())
    # Check if input valid
    if len(answer) == 4 and answer.isdigit():
        # Modify answer into list
        for i in range(4):
            answer_ls.append(int(answer[i]))
        print('answer_ls=', answer_ls)

        # Check if answer is correct and record the result
        if answer_ls == session['target']:
            check_result = '4A0B'
            session['check'].append([answer, check_result])
            message = "You Win!"

        # Check ?A?B and record the result
        else:
            tmp = session['target'].copy()
            print('tmp=',tmp)
            A = 0
            B = 0
            i = 0
            j = 0
            while i < len(tmp):
                if answer_ls[i] == tmp[i]:
                    A += 1
                    tmp.pop(i)
                    answer_ls.pop(i)
                else:
                    i += 1

            while j < len(tmp):
                if answer_ls[j] in tmp:
                    B += 1
                    tmp.remove(answer_ls[j])
                    answer_ls.pop(j)
                else:
                    j += 1

            check_result = str(A)+'A'+str(B)+'B'
            session['check'].append([answer, check_result])
            print('check_session', session['check'])
            print()

        return render_template("index.html", results=session['check'], the_row_results=the_row_results, message=message)

    # Invalid input
    else:
        print("input invalid")
        return render_template("index.html",check_result="Please input 4-digit number", results=session['check'], the_row_results=the_row_results, message=message)

if __name__ == '__main__':
    app.run(debug = True)
