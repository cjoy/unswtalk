#!/web/cs2041/bin/python3.6.3

# written by andrewt@cse.unsw.edu.au October 2017
# as a starting point for COMP[29]041 assignment 2
# https://cgi.cse.unsw.edu.au/~cs2041/assignments/UNSWtalk/

import os, re
from flask import Flask, render_template, session, request, redirect, url_for
import controller as ctrl

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def start():
    # protected route - check if user logged in
    if 'logged_in' not in session:
        return redirect('/login')

    return redirect('/feeds')


@app.route('/feeds', methods=['GET','POST'])
def feeds():
    # protected route - check if user logged in
    if 'logged_in' not in session:
        return redirect('/login')

    feeds = ctrl.GetUserFeeds(session['zid'])
    return render_template('feeds.html', title="My Feeds", feeds=feeds,
        getdetails=ctrl.GetUserDetails, GetProfilePic=ctrl.GetProfilePic,
        parseTime=ctrl.parseTime)


@app.route('/search/people', methods=['GET','POST'])
def search_people():
    # protected route - check if user logged in
    if 'logged_in' not in session:
        return redirect('/login')

    # get search query
    query = request.args.get('q')
    if query == None:
        query = ''

    # compute search results
    results = ctrl.SearchPeople(query)

    return render_template('search_people.html', title='Search People - "' + query + '"', 
        GetProfilePic=ctrl.GetProfilePic,
        results=results, query=query)
    

@app.route('/profile/<zid>', methods=['GET','POST'])
def profile(zid):
    # protected route - check if user logged in
    if 'logged_in' not in session:
        return redirect('/login')
        
    student_to_show = zid
    details = ctrl.GetUserDetails(student_to_show)
    posts = ctrl.GetUserPosts(student_to_show)

    courses = list(re.sub(r'(\(|\))', '', details['courses']).split(','))
    friends = list(re.sub(r'(\(|\)|\s)', '', details['friends']).split(','))

    return render_template('profile.html', title=details['full_name'],
        student_details=details, posts=reversed(posts),
        getdetails=ctrl.GetUserDetails, GetProfilePic=ctrl.GetProfilePic,
        parseTime=ctrl.parseTime,
        courses=courses, friends=friends)


@app.route('/login', methods=['GET','POST'])
def login():
    # test function
    feeds = ctrl.GetUserFeeds('z5195935')

    # error status is set to true
    status = True

    zid = request.form.get('zid')
    password = request.form.get('password')

    # check zid and password and set session
    if zid != None and password != None:
        if ctrl.GetUserDetails(zid)['password'] == password:
            session['logged_in'] = True
            session['zid'] = zid
            session['user_details'] = ctrl.GetUserDetails(zid)
            return redirect('/')
        else:
            status = False

    return render_template('login.html', title="Login", status=status)


@app.route('/register', methods=['GET','POST'])
def register():
    return render_template('register.html', title="Register")


@app.route('/logout', methods=['GET','POST'])
def logout():
    session.pop('logged_in', None)
    session.pop('zid', None)
    session.pop('user_details', None)
    return redirect('/login')


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
