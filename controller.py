import os
import glob
import yaml, json, sys
import re
from datetime import datetime
import operator
import random

students_dir = "static/dataset-large";

# Post Object
class Post:
    def __init__(self, fname):
        with open(fname) as f:
            for field in f:
                if field.startswith('from:'):
                    self._from = field[len('from: '):].rstrip()
                if field.startswith('message:'):
                    self.message = field[len('message: '):].rstrip()
                if field.startswith('time:'):
                    self.time = field[len('time: '):].rstrip()
                if field.startswith('longitude:'):
                    self.longitude = field[len('longitude: '):].rstrip()
                if field.startswith('latitude:'):
                    self.latitude = field[len('latitude: '):].rstrip()


# allow quotes in yaml files
def literalFile(content):
    content = re.sub('"','\\"',content)
    content = re.sub(':','',content)
    return content

# TODO: parse datatime (for posts etc)
def parseTime(tstamp):
    return tstamp

# get user image
def GetProfilePic(zid):
    profile_pic = 'http://www.freeiconspng.com/uploads/profile-icon-9.png'
    file_path = os.path.join(students_dir, zid, "img.jpg")
    if os.path.exists(file_path):
        profile_pic = '/' + file_path
    return profile_pic



# Get user details, given zid
def GetUserDetails(zid):
    details_filename = os.path.join(students_dir, zid, "student.txt")
    details = {}
    if os.path.exists(details_filename):
        with open(details_filename) as f:
            details = yaml.load(f.read())
    return details


# Get all users (array of user objects returned)
def GetAllUsers():
    users = []
    for user in sorted(os.listdir(students_dir)):
        users.append(GetUserDetails(user))
    return users


# Search for people
def SearchPeople(query):
    results = []
    for user in GetAllUsers():
        if query.lower() in user['full_name'].lower():
            results.append(user)
    
    return results

# get post thread, given post id (eg. postid: dataset-medium/z5191841/12.txt)
def GetPostThread(postid):
    comments_array = []
    # loop through comments
    comment_files = glob.glob(postid.split('.txt')[0]+'-[0-99].txt')
    for comment in comment_files:
        replies_array = []
        comment_obj = {
            'id': comment,
            'content': Post(comment),
            'replies': replies_array
        }
        
        # loop through replies
        reply_files = glob.glob(comment.split('.txt')[0]+'-[0-99].txt')
        for reply in reply_files:
            reply_obj = {
                'id': reply,
                'content': Post(reply),
            }
            replies_array.append(reply_obj)

        comments_array.append(comment_obj)

    # create post object
    post_obj = {
        'id': postid,
        'content': Post(postid),
        'comments': comments_array
    }

    return post_obj

# Get user posts, comments to those posts and replies to those posts
def GetUserPosts(zid):
    print("Getting posts for", zid)
    user_dir = os.path.join(students_dir, zid)

    posts = []
    for post in glob.glob(user_dir+'/[0-99].txt'):
        posts.append(GetPostThread(post))

    return posts


# Get user feeds
def GetUserFeeds(zid):
    posts = []

    # get user recent posts
    user_dir = os.path.join(students_dir, zid)
    for user_post in reversed(glob.glob(user_dir+'/[0-99].txt')):
        posts.append(GetPostThread(user_post))

    # loop though friends
    user_details = GetUserDetails(zid)
    friends = list(re.sub(r'(\(|\)|\s)', '', user_details['friends']).split(','))
    for friend in friends:
        # get friend's recent posts
        friend_dir = os.path.join(students_dir, friend)
        for friend_post in reversed(glob.glob(friend_dir+'/[0-99].txt')):
            posts.append(GetPostThread(friend_post))

    # MENTIONS DISABLED - WAY TOO SLOW
    # loop through all mentions
    # all_students = sorted(os.listdir(students_dir))
    # for post in all_students:
    #     # get friend's recent posts
    #     posts_dir = os.path.join(students_dir, post)
    #     for all_post in reversed(glob.glob(posts_dir+'/[0-99].txt')):
    #         posts_content = GetPostThread(all_post)
    #         # append if mentioned
    #         if zid in posts_content['content'].message:
    #             posts.append(posts_content)
    
    return reversed(posts)
