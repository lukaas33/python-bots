"""
Reddit bot for replying to the phrase 'random john|hank' with a random sentence.
Sentences are generated with markovify and are based on transcripts from https://nerdfighteria.info/.
Made with data available on 2018-04-10.
"""

# > Imports
from . import sentence
import praw
import bmemcached

import re
import string
import time
import os


# Main functionality
def main():
    # >> Vars
    cache = bmemcached.Client(os.environ.get('MEMCACHEDCLOUD_SERVERS').split(','), os.environ.get('MEMCACHEDCLOUD_USERNAME'), os.environ.get('MEMCACHEDCLOUD_PASSWORD'))


    gens = {
    "John": sentence.gen('john-green'),
    "Hank": sentence.gen('hank-green')
    }

    template = string.Template('''
    > $text
    -- $name

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
    def reply(target, comment, start):
        try:
            line = sentence.sentence(gens[target], start)

            print('Reply:', line)

            if line:
                rep = comment.reply(template.substitute(name=target + ' Green', text=line))
                store(rep.id)  # Don't reply to self

            store(comment.id)

        except praw.exceptions.APIException as err:
            print('Error:', err)
            time.sleep(60 * 5)  # Wait until ratelimit ended
            reply(target, comment, start)
        except Exception as err:
            print(err)
            time.sleep(60 * 10)
            main()  # Restart after waiting


    # Run the bot
    def run_bot(reddit):

        # Checks all comments
        for comment in reddit.subreddit('nerdfighters').stream.comments():
            if comment.id not in replied:
                print('Comment:', comment.body)
                text = comment.body.lower()
                target = None

                if "random john" in text:
                    target = 'John'
                if "random hank" in text:
                    target = 'Hank'

                if target:
                    parts = text.split(target.lower())
                    parts = parts[1].strip().split(' ')
                    if parts[0]:
                        start = re.sub(r'\W+', '', parts[0])  # Only alphanumerical
                        start = start.title()
                    else:
                        start = None



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
