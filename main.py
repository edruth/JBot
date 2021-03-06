__version__ = '0.1.0'

import re
import logging
from time import sleep, time
from logging.config import dictConfig
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

import telegram

from conf.log_conf import LOG_CONF
from conf import configuration as cfg

logger = logging.getLogger(__name__)


def get_updates(bot, update_id):
    last_update_id = 0
    updates = bot.getUpdates(offset=update_id)
    if updates:
        last_update_id = updates[-1].update_id

    for update in updates:
        text = update.message.text
        if text is None:
            continue
        for bot_address in cfg.BOT_ADDRESS_SET:
            if re.match(bot_address, text, re.IGNORECASE):
                update.message.text = re.sub(bot_address, '', text)
                return update, update.update_id + 1

    return [], last_update_id + 1


def process_messages(bot):
    update_id = None
    last_request = 0
    with ThreadPoolExecutor(3) as executor:
        while True:
            update, update_id = get_updates(bot, update_id)
            if update:
                message = update.message.text
                split_message = []

                # create all possible commands from message
                comb = ''
                for word in message.split():
                    comb += word.lower() + ' '
                    split_message.append(comb.strip())

                for ability in cfg.abilities:
                    ability_methods = ability.get_commands()
                    for method_name, commands in ability_methods.items():
                        for command in commands:
                            if command.lower() in split_message:
                                if last_request + cfg.SLEEP_BETWEEN_REQUESTS > time():
                                    bot.sendMessage(chat_id=update.message.chat_id, text="Please don't abuse me")
                                    break
                                last_request = time()
                                request = message.replace(command, '')

                                logger.debug("executing ability: {} with request: {}".format(ability.__name__, request))
                                run_method = getattr(ability(bot, update, cfg.abilities), method_name)
                                executor.submit(run_method(request.lower(), command.lower()))
                                break

                        else:  # breaking from inner loop
                            continue
                        break

            sleep(cfg.SLEEP_BETWEEN_UPDATES)


def main():
    dictConfig(LOG_CONF)
    bot = telegram.Bot(token=cfg.TELEGRAM_TOKEN)

    # reset accumulated messages
    updates = bot.getUpdates()
    if updates:
        last_update_id = updates[-1].update_id
        bot.getUpdates(offset=last_update_id+1)

    with ProcessPoolExecutor(1) as executor:
        executor.submit(process_messages(bot))


if __name__ == '__main__':
    try:
        main()
    except Exception:
        logger.exception('sleeping due to unhandled exception')
        sleep(cfg.SLEEP_BETWEEN_EXCEPTIONS)
        main()
