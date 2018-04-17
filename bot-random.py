"""
Reddit bot for replying to the phrase 'random john|hank' with a random sentence.
Sentences are generated with markovify and are based on transcripts from https://nerdfighteria.info/.
Made with data available on 2018-04-10.
"""

# > Imports
import praw
import config
import green

import math
import string
import time


# > Vars
gens = {
    "John": green.sentences('john-green', math.inf),
    "Hank": green.sentences('hank-green', math.inf)
}

template = string.Template('''
> $text
- $name

I am a bot. This sentence is randomly generated and based on Vlogbrothers transcripts.
For more info or comments [email me](mailto:lukaas9000@gmail.com).''')

# Get past replies on restart
replied = set()
with open('replied.txt', 'r', encoding='utf-8') as file:
    for id in file.read().split('\n'):
        if id:  # Not empty
            replied.add(id)


# > Functions
# Login
def authenticate():
    # Enter credentials
    reddit = praw.Reddit(
        client_id=config.id,
        client_secret=config.secret,
        password=config.passw,
        user_agent='/r/nerdfighters, randomNerdfighter.Bot, v1.0, by /u/lukaas33',
        username='randomNerdfighterbot'
    )
    return reddit

# Store ids
def store(id):
    global replied

    replied.add(id)
    with open('replied.txt', 'a', encoding='utf-8') as file:
        file.write(id + '\n')
    print(id)

# Replies
def reply(target, comment):
    try:
        line = next(gens[target])

        print('Comment:', comment.body.lower())
        print('Reply:', line)

        re = comment.reply(template.substitute(name=target + 'Green', text=line))

        store(re.id)  # Don't reply to self
        store(comment.id)
    except praw.exceptions.APIException as err:
        print('Error:', err)
        time.sleep(60 * 5)  # Wait until ratelimit ended
        reply(target, comment)
    except Exception as err:
        print(err)
        time.sleep(60 * 10)
        main()  # Restart after waiting


# Run the bot
def run_bot(reddit):

    # Checks all comments
    for comment in reddit.subreddit('nerdfighters').stream.comments():
        text = comment.body.lower()

        if comment.id not in replied:
            if "random john" in text:
                reply('John', comment)
            if "random hank" in text:
                reply('Hank', comment)


# Main functionality
def main():
    try:
        # Bot runs
        reddit = authenticate()
        run_bot(reddit)
    except Exception as err:
        print(err)
        time.sleep(60 * 10)
        main()  # Restart after waiting



# > Execute
# Run straight from command line, run every 15 minutes
if __name__ == '__main__':
    main()
