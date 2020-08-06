import praw
from pushbullet import Pushbullet
import os
import time
from config import token

# Define Reddit
reddit = praw.Reddit('bot1', config_interpolation="basic")

pb = Pushbullet(token)
reddit.read_only = True  # set our reddit instance to read only.. realistically was unnecessary
# What are we interested in
searchList = ['jpc', 'crye', 'criterion', 'rosco']

if not os.path.isfile("posts_checked.txt"):  # check to see if we have a file and not create an array
    posts_read = []
else:  # Load the existing file if it already exists
    with open("posts_checked.txt", "r") as f:
        posts_read = f.read()
        posts_read = posts_read.split("\n")
        posts_read = list(filter(None, posts_read))

# Meat and potatoes
iteration = 0
while True:
    try:
        for submission in reddit.subreddit("gundeals").new(limit=100):  # Get the last 1000 from the gun deals subreddit
            if submission.id not in posts_read:
                if any(matches in submission.title.lower() for matches in searchList):
                    pb.push_link(title=submission.title, url=submission.url)
                    print(submission.title)
                    posts_read.append(submission.id)  # Add the submission we sent a notification for
                    # Update our file
                    with open("posts_checked.txt", "w") as f:
                        for post_id in posts_read:
                            f.write(post_id + "\n")

        print("Iteration #: ", iteration)
        time.sleep(60)
        iteration += 1
    except ValueError:
        print("Oh Shit")
        time.sleep(60)
