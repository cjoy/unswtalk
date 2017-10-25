import os
import glob
import yaml, json, sys

students_dir = "dataset-small";

# helper functions
def GetUserDetails(zid):
    details_filename = os.path.join(students_dir, zid, "student.txt")
    details = {}
    with open(details_filename) as f:
        details = yaml.load(f.read())
    return details

def GetUserPosts(zid):
    posts = []
    user_dir = os.path.join(students_dir, zid)
    post_files = glob.glob(user_dir+'/[0-9].txt')
    for post in post_files:
        print(post)
        reply_files = glob.glob(post.split('.txt')[0]+'-[0-9].txt')
        for reply in reply_files:
            print(" ", reply)
            reply_files = glob.glob(post.split('.txt')[0]+'-[0-9].txt')

        # with open(post) as f:
        #     posts.append(yaml.load(f.read()))

    return posts