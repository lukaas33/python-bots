"""
Reddit bot for replying to the phrase 'random john|hank' with a random sentence.
Sentences are generated with markovify and are based on transcripts from https://nerdfighteria.info/.
Made with data available on 2018-04-10.
"""

# > Imports
from . import sentence
import praw
import bmemcached

import math
import string
import time
import os


# Main functionality
def main():
    # >> Vars
    cache = bmemcached.Client(os.environ.get('MEMCACHEDCLOUD_SERVERS').split(','), os.environ.get('MEMCACHEDCLOUD_USERNAME'), os.environ.get('MEMCACHEDCLOUD_PASSWORD'))


    gens = {
        "John": sentence.sentences('john-green', math.inf),
        "Hank": sentence.sentences('hank-green', math.inf)
    }

    template = string.Template('''
    > $text
    - $name

    I am a bot. This sentence is randomly generated and based on Vlogbrothers transcripts.
    For more info or comments [email me](mailto:lukaas9000@gmail.com).
    ''')

    # Get past replies on restart
    init = set()

    with open("C:\\Users\\Lucas\\Documents\\Git\\python-bots\\bots\\green\\replied.txt", 'r', encoding='utf-8') as file:
        for id in file.read().split('\n'):
            if id:  # Not empty
                init.add(id)

    cache.set('replied', '-'.join(init))

    data = cache.get('replied')
    if data:
        replied = set(data.split('-'))
    else:
        replied = set()
    print(replied)


    # >> Functions
    # Login
    def authenticate():
        # Enter credentials
        reddit = praw.Reddit(
            client_id=os.environ.get('ID', None),
            client_secret=os.environ.get('secret', None),
            password=os.environ.get('passw', None),
            user_agent='/r/nerdfighters, randomNerdfighter.Bot, v1.0, by /u/lukaas33',
            username='randomNerdfighterbot'
        )
        print("Logged in")
        return reddit

    # Store ids
    def store(id):
        global replied

        replied.add(id)
        cache.replace('replied', '-'.join(replied))

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


    try:
        # Bot runs
        print("Logging in")
        reddit = authenticate()
        run_bot(reddit)
    except Exception as err:
        print(err)
        time.sleep(60 * 10)
        main()  # Restart after waiting



# >> Execute
# Run straight from command line
if __name__ == '__main__':
    main()
