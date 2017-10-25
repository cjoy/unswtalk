#!/web/cs2041/bin/python3.6.3

# written by andrewt@cse.unsw.edu.au October 2017
# as a starting point for COMP[29]041 assignment 2
# https://cgi.cse.unsw.edu.au/~cs2041/assignments/UNSWtalk/

import os
from flask import Flask, render_template, session

students_dir = "dataset-small";

import controller as ctrl
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
@app.route('/start', methods=['GET','POST'])
def start():
    n = session.get('n', 0)
    students = sorted(os.listdir(students_dir))
    student_to_show = students[n % len(students)]
    details = ctrl.GetUserDetails(student_to_show)
    print(ctrl.GetUserPosts(student_to_show))
    session['n'] = n + 1
    return render_template('start.html', student_details=details)

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
