import praw
import obot
from time import strftime


NUMCOMMENTS = 0
SETPHRASES = ["pelican", "pelicans"]
SUBBLACKLIST = ["nba", "test"]
COMMLIMIT = 100
COMMREPLY = "Don't fuck with the [pelicans](https://www.youtube.com/watch?v=jWxIOdt-V8Y)"
USERNAME = "SecretAg3nt"

commDone = set()
subDone = set()


# Creates msg from keyword and comment passed in
def create_message(NUMCOMMENTS, key, comment):
    return str(NUMCOMMENTS) + ") " + strftime("%Y-%m-%d %H:%M:%S") + " Someone is talking about \"" + key + "\": " + comment.author.name + " " + comment.permalink


def send_update(NUMCOMMENTS, key, comment, USERNAME):
    print(create_message(NUMCOMMENTS, key, comment))
    subject = "Someone is talking about " + key
    r.send_message(USERNAME, subject, create_message(NUMCOMMENTS, key, comment))
    print("Message Sent to " + USERNAME)


r = obot.login()
print("Logged in")
print(strftime("%Y-%m-%d %H:%M:%S") + " Searching for: " + str(SETPHRASES))

while True:
    try:
        for comment in praw.helpers.comment_stream(r, 'all', limit=COMMLIMIT, verbosity=0):
            if comment.id not in commDone:
                commDone.add(comment.id)
                for word in comment.body.lower().split():
                    for key in SETPHRASES:
                        if word == key:
                            NUMCOMMENTS += 1
                            send_update(NUMCOMMENTS, key, comment, USERNAME)
                            if comment.submission.id not in subDone and comment.subreddit.display_name not in SUBBLACKLIST:
                                comment.reply(COMMREPLY)
                                print("Replied to comment")
                                subDone.add(comment.submission.id)
                            else:
                                print("Reply not sent, subreddit black-listed.")
                                subDone.add(comment.submission.id)

    except:
        pass
