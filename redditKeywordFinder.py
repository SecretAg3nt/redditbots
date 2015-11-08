import praw
from time import strftime
import obot

# configurable settings
SETPHRASES = ["reddit"]
COMMLIMIT = 100
USERNAME = "SecretAg3nt"


commDone = set()
NUMCOMMENTS = 0


# Creates msg from keyword and comment passed in
def create_message(NUMCOMMENTS, key, comment):
    return str(NUMCOMMENTS) + ") " + strftime("%Y-%m-%d %H:%M:%S") + " Someone is talking about \"" + key + "\": " + comment.author.name + " " + comment.permalink

# Starts loop by printing timestamp, logging in
print(strftime("%Y-%m-%d %H:%M:%S"))
r = obot.login()
print("Logged in")

while True:
    try:
        print("Starting comment stream")
        for comment in praw.helpers.comment_stream(r, 'all', limit=COMMLIMIT, verbosity=0):
            # Checks if comment has been checked yet
            if comment.id not in commDone:
                commDone.add(comment.id)
            # Compares words in the comment to all the keywords
            for word in comment.body.lower().split():
                for key in SETPHRASES:
                    # If a word matches, sends msg with link to comment to USERNAME, and displays so on screen
                    if word == key.lower():
                        NUMCOMMENTS = NUMCOMMENTS + 1
                        print(create_message(NUMCOMMENTS, key, comment))
                        subject = "Someone is talking about " + key
                        r.send_message(USERNAME, subject, create_message(NUMCOMMENTS, key, comment))
                        print("Message Sent")
    except:
        pass
