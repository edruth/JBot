
import time

from abilities.ability_base import AbilityBase
from utils.decorators import command
from utils.objects import CommandObj as co


class Flow(AbilityBase):

    flow = {'name': '', 'flow': '', 'time': ''}

    @command(co('set flow', 'set the flow'),)
    def set_flow(self, request, command=None):

        if not request:
            self.reply('Cant set empty flow!')
            return

        Flow.flow['name'] = self.update.message.from_user.first_name
        Flow.flow['flow'] = request
        Flow.flow['time'] = time.strftime("%d/%m/%y %H:%M")
        self.reply('flow set to: {}'.format(request))

    @command(co('whats the flow', 'Show the flow'),)
    def get_flow(self, request=None, command=None):
        self.reply('{name} set the flow at {time} to: {flow}'.format(**Flow.flow))