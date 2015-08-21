from abilities.wikipedia import Wikipedia
from abilities.flow import Flow
from abilities.jokes import Jokes
from abilities.general import General

TELEGRAM_TOKEN = "123272225:AAGcb712Y5-qIUOgVC5a5C2nkSkENP7DEo0"

SLEEP_BETWEEN_REQUESTS = 10  # seconds
SLEEP_BETWEEN_UPDATES = 1  # seconds
SLEEP_BETWEEN_EXCEPTIONS = 600  # seconds


BOT_ADDRESS_SET = {'^j ', '^yo j ', '^jj ', '^jb ', }
abilities = (General, Wikipedia, Flow, Jokes)

