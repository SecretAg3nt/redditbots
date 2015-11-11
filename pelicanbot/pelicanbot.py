import praw
import obot
from time import strftime


# Creates msg from keyword and comment passed in
def create_message(comment):
    return "PelicanBot found someone talking about pelicans! " + comment.author.name + " " + comment.permalink


def terminal_prompt(comment, NUMCOMMENT):
    return str(NUMCOMMENT) + ") " + comment.author.name + " - r/" + comment.subreddit.display_name + "\n"


def send_update(r, key, comment, USERNAME, NUMCOMMENT):
    print(terminal_prompt(comment, NUMCOMMENT))
    subject = "Someone is talking about " + key + "!"
    r.send_message(USERNAME, subject, create_message(comment))


def run():

    KEYPHRASES = ["pelican", "pelicans"]
    SUBBLACKLIST = ["nba"]
    COMMLIMIT = 100
    COMMREPLY = "Don't fuck with the [pelicans](https://www.youtube.com/watch?v=jWxIOdt-V8Y)"
    USERNAME = "SecretAg3nt"
    NUMCOMMENT = 0

    commDone = set()
    subDone = set()
    r = obot.login()

    print("Logged in")
    print(strftime("%Y-%m-%d %H:%M:%S") + " Searching for: " + str(KEYPHRASES))

    while True:
       # try:
            for comment in praw.helpers.comment_stream(r, 'all', limit=COMMLIMIT, verbosity=0):
                if comment.id not in commDone:
                    commDone.add(comment.id)
                    for word in comment.body.lower().split():
                        for key in KEYPHRASES:
                            if word == key:
                                if comment.subreddit.display_name not in SUBBLACKLIST:
                                    if comment.submission.id not in subDone:
                                        NUMCOMMENT += 1
                                        comment.reply(COMMREPLY)
                                        send_update(r, key, comment, USERNAME, NUMCOMMENT)
                                        subDone.add(comment.submission.id)

                                    else:
                                        print("Reply not sent, submission already replied to. " + comment.permalink + "\n")
                                else:
                                    print("Reply not sent, subreddit black-listed. " + comment.subreddit.display_name + "\n")
                                    subDone.add(comment.submission.id)


      #  except:
           # pass

if __name__ == "__main__":
    run()
