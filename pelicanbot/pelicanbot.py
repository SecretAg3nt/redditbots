import praw
from time import strftime
import obot


commDone = set()
subDone = set()
NUMCOMMENTS = 0
SETPHRASES = ["pelican"]
COMMLIMIT = 100

print(strftime("%Y-%m-%d %H:%M:%S"))

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
                        msg = str(NUMCOMMENTS) + ") *" + strftime("%Y-%m-%d %H:%M:%S") + "* Someone is talking about \"" + key + "\": " + comment.author.name + " " + comment.permalink
                        print(msg)
                        subject = "Someone is talking about \"" + key
                        r.send_message('SecretAg3nt', subject, msg)
                        print("Message Sent")
                        if comment.submission.id not in subDone:
                            comment.reply("Don't fuck with [pelicans](https://www.youtube.com/watch?v=jWxIOdt-V8Y)")
                            print("Replied to comment")
                            subDone.add(comment.submission.id)

    except:
        pass
