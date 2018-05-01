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
        print("Logged in", flush=True)
        return reddit

    # Store ids
    def store(id):
        print(id, flush=True)

        replied.add(id)
        cache.set('replied', '-'.join(replied))

    # Replies
    def reply(target, comment, start):
        try:
            line = sentence.sentence(gens[target], start)
            print('Reply:', line, flush=True)

            if line:
                rep = comment.reply(template.substitute(name=target + ' Green', text=line))
                store(rep.id)  # Don't reply to self

            store(comment.id)

        except praw.exceptions.APIException as err:
            print('Error:', err, flush=True)
            time.sleep(60 * 5)  # Wait until ratelimit ended
            reply(target, comment, start)

        except Exception as err:
            print(err, flush=True)
            time.sleep(60 * 10)
            main()  # Restart after waiting


    # Run the bot
    def run_bot(reddit):
        def find_start(text, target):
            parts = text.lower().split(target.lower())
            parts = parts[1].strip().split(' ')
            if parts[0]:
                start = re.sub(r'\W+', '', parts[0])  # Only alphanumerical
                start = start.title()
            else:
                start = None

            return start

        # Checks all comments
        for comment in reddit.subreddit('nerdfighters').stream.comments():
            if comment.id not in replied:
                text = str(comment.body.encode(encoding='UTF-8', errors='replace'))
                print('Comment:', text, flush=True)

                if 'random john' in text.lower():
                    target = 'John'
                    start = find_start(text, target)
                    reply(target, comment, start)
                if 'random hank' in text.lower():
                    target = 'Hank'
                    start = find_start(text, target)
                    reply(target, comment, start)


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
    data = cache.get('replied')
    if data:
        replied = set(data.split('-'))
    else:
        replied = set()
    print(replied, flush=True)


    # >>> Execute
    try:
        # Bot runs
        print("Logging in", flush=True)
        reddit = authenticate()
        run_bot(reddit)
    except Exception as err:
        print(err, flush=True)
        time.sleep(60 * 10)
        main()  # Restart after waiting



# Run straight from command line
if __name__ == '__main__':
    main()
