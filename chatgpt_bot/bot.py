import asyncio
import re

import discord

from .chat_gpt import ChatGPT



class Bot(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')


    async def on_message(self, message: discord.Message):
        await self.ask_gpt(message)

    
    async def ask_gpt(self, message: discord.Message):

        def _ask_gpt(message: str) -> str:
            try:
                gpt = ChatGPT()
                return gpt.ask(message)
            except Exception as e:
                return (
                    f"```diff\n- Falha durante durante " 
                    f"a solicitação: {e}\n```"
                )

        content: str = message.content

        if not content.lower().startswith("/gpt"):
            return None
        
        content = re.sub(
            '/gpt', '', message, count=1, flags=re.IGNORECASE)

        if not content.strip():
            return None
        
        try:
            await message.add_reaction(
                self.get_emoji(1057412600696164442))
        except:
            pass

        response = await asyncio.get_running_loop()\
            .run_in_executor(None, _ask_gpt, message)

        await message.channel.send(response)
        await message.clear_reactions()
