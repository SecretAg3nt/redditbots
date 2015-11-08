import praw
import obot
from time import strftime


NUMCOMMENTS = 0
SETPHRASES = ["pelican", "pelicans"]
COMMLIMIT = 100
COMMREPLY = "Don't fuck with [pelicans](https://www.youtube.com/watch?v=jWxIOdt-V8Y)"
USERNAME = "SecretAg3nt"

commDone = set()
subDone = set()


# Creates msg from keyword and comment passed in
def create_message(NUMCOMMENTS, key, comment):
    return str(NUMCOMMENTS) + ") " + strftime("%Y-%m-%d %H:%M:%S") + " Someone is talking about \"" + key + "\": " + comment.author.name + " " + comment.permalink

print(strftime("%Y-%m-%d %H:%M:%S") + " Searching for: " + str(SETPHRASES))
r = obot.login()
print("Logged in")

while True:
    try:
        for comment in praw.helpers.comment_stream(r, 'all', limit=COMMLIMIT, verbosity=0):
            if comment.id not in commDone:
                cbody = comment.body.lower()
            cwords = cbody.split()
            commDone.add(comment.id)
            for word in cwords:
                for key in SETPHRASES:
                    if word == key:
                        NUMCOMMENTS = NUMCOMMENTS + 1
                        print(create_message(NUMCOMMENTS, key, comment))
                        subject = "Someone is talking about " + key
                        r.send_message(USERNAME, subject, create_message(NUMCOMMENTS, key, comment))
                        print("Message Sent to " + USERNAME)
                        if comment.submission.id not in subDone:
                            comment.reply(COMMREPLY)
                            print("Replied to comment")
                            subDone.add(comment.submission.id)

    except:
        pass
