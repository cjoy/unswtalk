import os
import glob
import yaml, json, sys
import re
from datetime import datetime

students_dir = "static/dataset-small";


# allow quotes in yaml files
def literalFile(content):
    content = re.sub('"','\\"',content)
    return content

# TODO: parse datatime (for posts etc)
def parseTime(tstamp):
    return tstamp

# get user image
def GetProfilePic(zid):
    file_path = os.path.join(students_dir, zid, "img.jpg")
    profile_pic = 'http://www.freeiconspng.com/uploads/profile-icon-9.png'
    if os.path.exists(file_path):
        profile_pic = file_path
    # print(profile_pic)
    return profile_pic



# Get user details, given zid
def GetUserDetails(zid):
    details_filename = os.path.join(students_dir, zid, "student.txt")
    details = {}
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


# Get user posts, comments to those posts and replies to those posts
def GetUserPosts(zid):
    print("Getting posts for", zid)
    posts = []
    user_dir = os.path.join(students_dir, zid)
    post_files = glob.glob(user_dir+'/[0-9].txt')
    # loop through posts
    for post in post_files:
        post_file = open(post,'r')
        post_content = yaml.safe_load(literalFile(post_file.read()))
        post_file.close()

        comments_array = []
        post_obj = {
            'id': post,
            'content': post_content,
            'comments': comments_array
        }
        # loop through comments
        comment_files = glob.glob(post.split('.txt')[0]+'-[0-9].txt')
        for comment in comment_files:
            comment_file = open(comment,'r')
            comment_content = yaml.safe_load(literalFile(comment_file.read()))
            comment_file.close()

            replies_array = []
            comment_obj = {
                'id': comment,
                'content': comment_content,
                'replies': replies_array
            }
            # loop through replies
            reply_files = glob.glob(comment.split('.txt')[0]+'-[0-9].txt')
            for reply in reply_files:
                reply_file = open(reply,'r')
                reply_content = yaml.safe_load(literalFile(reply_file.read()))
                reply_file.close()
                reply_obj = {
                    'id': reply,
                    'content': reply_content,
                }
                replies_array.append(reply_obj)

            comments_array.append(comment_obj)

        posts.append(post_obj)

    return posts