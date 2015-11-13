import praw
import obot
from time import strftime
import os


def terminal_prompt(comment, NUMCOMMENT):
    print(str(NUMCOMMENT) + ") " + comment.author.name + " - r/" + comment.subreddit.display_name + "\n")


def run():

    KEYPHRASES = ["pelican", "pelicans"]
    SUBBLACKLIST = ["nba"]
    COMMLIMIT = 100
    COMMREPLY = "Don't fuck with the [pelicans](https://www.youtube.com/watch?v=jWxIOdt-V8Y)"
    NUMCOMMENT = 0

    commDone = set()
    subDone = set()
    r = obot.login()

    print("Logged in")
    print(strftime("%Y-%m-%d %H:%M:%S") + " Searching for: " + str(KEYPHRASES))

    while True:
        try:
            for comment in praw.helpers.comment_stream(r, 'all', limit=COMMLIMIT, verbosity=1):
                if comment.id not in commDone:
                    commDone.add(comment.id)
                    for word in comment.body.lower().split():
                        for key in KEYPHRASES:
                            if word == key:
                                if comment.subreddit.display_name not in SUBBLACKLIST:
                                    if comment.submission.id not in subDone:
                                        NUMCOMMENT += 1
                                        comment.reply(COMMREPLY)
                                        subDone.add(comment.submission.id)
                                        terminal_prompt(comment, NUMCOMMENT)
                                    else:
                                        print("Reply not sent, submission already replied to. " + "\n")
                                else:
                                    print("Reply not sent, subreddit black-listed. " + comment.subreddit.display_name + "\n")
                                    subDone.add(comment.submission.id)

        except:
            pass

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    run()
