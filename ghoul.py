#meta developers: @confuseeeed
import io, inspect
from .. import loader, utils
from asyncio import sleep

@loader.tds
class GULMod(loader.Module):
    strings = {'name': 'Гуль'}
    
    async def ghoulcmd(self, message):
        x = 1000
        await sleep(2)
        while x >0:
            await message.client.send_message(message.to_id, str(x) + " - 7 = " + str(x-7))
            x -= 7
            await sleep(0.01)
