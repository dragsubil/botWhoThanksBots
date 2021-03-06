#!usr/bin/python3

"""
A Reddit bot that thanks other bots

Note: Since the bot is on a new account, it cannot
make a comment more than once every 10 minutes.
"""

import praw
import time

botlist = [ 'AnimalFactsBot', 'remindmebot', 'automoderator', 'totesmessenger',
            'TweetsInCommentsBot', 'GoodBot_BadBot', 'haikubot-1911',
           ]
replied_comments = {}
comment_string = """
Thank you {}!

----
^(Because bots deserve gratitude.)

"""


def post_reply(botname, comment):
    try:
        if replied_comments[comment.id]:
            return
    except KeyError:
        try:
            comment.reply(comment_string.format(botname))
        except Exception as e:
            print("Moving to the next bot because exception occured:", str(e))
            return

        replied_comments[comment.id] = True
        print("Thanked {}. id: {}".format(botname, comment.id))


def thank_the_bots():
    for botname in botlist:
        try:
            reddit = praw.Reddit('thankerbot')
            bot_object = reddit.redditor(botname)
            # bot_new_submissions includes posts and comments
            bot_new_submissions = bot_object.new(limit=1)
            for submission in bot_new_submissions:
                print("retrieving next comment")
                if isinstance(submission, praw.models.reddit.comment.Comment):
                    post_reply(botname, submission)
                    print("waiting 10 minutes because reddit doesn't want spam")
                    time.sleep(600)
        except Exception as e:
            print("some exception occured so moving on:", e)


if __name__ == '__main__':
    while True:
        thank_the_bots()
