import praw
import obot
from time import strftime


KEYPHRASES = ["pelican", "pelicans"]
SUBBLACKLIST = ["nba", "test"]
COMMLIMIT = 100
COMMREPLY = "Don't fuck with the [pelicans](https://www.youtube.com/watch?v=jWxIOdt-V8Y)"
USERNAME = "SecretAg3nt"


# Creates msg from keyword and comment passed in
def create_message(comment):
    return "PelicanBot found someone talking about pelicans! " + comment.author.name + " " + comment.permalink


def send_update(key, comment, USERNAME):
    print(create_message(comment) + "\n")
    subject = "Someone is talking about " + key + "!"
    r.send_message(USERNAME, subject, create_message(key, comment))
    print("Message Sent to " + USERNAME)

commDone = set()
subDone = set()
r = obot.login()
print("Logged in")
print(strftime("%Y-%m-%d %H:%M:%S") + " Searching for: " + str(KEYPHRASES))

while True:
    try:
        for comment in praw.helpers.comment_stream(r, 'all', limit=COMMLIMIT, verbosity=0):
            if comment.id not in commDone:
                commDone.add(comment.id)
                for word in comment.body.lower().split():
                    for key in KEYPHRASES:
                        if word == key:
                            if comment.subreddit.display_name not in SUBBLACKLIST:
                                if comment.submission.id not in subDone:
                                    comment.reply(COMMREPLY)
                                    send_update(key, comment, USERNAME)
                                    print("Replied to comment")
                                    subDone.add(comment.submission.id)
                                else:
                                    print("Reply not sent, submission already replied to. " + comment.permalink)
                            else:
                                print("Reply not sent, subreddit black-listed. " + comment.permalink)
                                subDone.add(comment.submission.id)

    except:
        pass
