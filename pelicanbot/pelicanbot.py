import praw
import obot
from time import strftime
import os


class pelicanBot(object):

    def __init__(self):
        self.KEYPHRASES = ["pelican", "pelicans"]
        self.SUBBLACKLIST = ["nba"]
        self.COMMLIMIT = 100
        self.COMMREPLY = "Don't fuck with the [pelicans](https://www.youtube.com/watch?v=jWxIOdt-V8Y)"
        self.NUMCOMMENT = 0
        self.commDone = set()
        self.subDone = set()
        self.r = obot.login()

    def terminal_prompt(self, comment, NUMCOMMENT):
        print(str(NUMCOMMENT) + ") " + comment.author.name + " - r/" + comment.subreddit.display_name + "\n")

    def run(self):
        print("Logged in")
        print(strftime("%Y-%m-%d %H:%M:%S") + " Searching for: " + str(self.KEYPHRASES))

        while True:
            try:
                for comment in praw.helpers.comment_stream(self.r, 'all', limit=self.COMMLIMIT, verbosity=1):
                    if comment.id not in self.commDone:
                        self.commDone.add(comment.id)
                        for word in comment.body.lower().split():
                            for key in self.KEYPHRASES:
                                if word == key:
                                    if comment.subreddit.display_name not in self.SUBBLACKLIST:
                                        if comment.submission.id not in self.subDone:
                                            self.NUMCOMMENT += 1
                                            comment.reply(self.COMMREPLY)
                                            self.subDone.add(comment.submission.id)
                                            self.terminal_prompt(comment, self.NUMCOMMENT)
                                        else:
                                            print("Reply not sent, submission already replied to. " + "\n")
                                    else:
                                        print("Reply not sent, subreddit black-listed. r/" + comment.subreddit.display_name + "\n")
                                        self.subDone.add(comment.submission.id)

            except:
                pass

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    pelbot = pelicanBot()
    pelbot.run()
