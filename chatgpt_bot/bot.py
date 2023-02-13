import asyncio
import re

import discord

from .chat_gpt import ChatGPT



class Bot(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')


    async def on_message(self, message: discord.Message):
        if not message.author.bot:
            await self.ask_gpt(message)

    
    async def ask_gpt(self, message: discord.Message):
        
        gpt = ChatGPT(id_user_discord=str(message.author.id))

        def _ask_gpt(_message: str) -> str:
            try:
                if gpt.api_key is None:
                    return None

                return gpt.ask(_message)

            except Exception as e:
                return (
                    f"```diff\n- Falha durante durante " 
                    f"a solicitação: {e}\n```"
                )

        content: str = message.content

        if not content.lower().startswith("/gpt"):
            return None
        
        content = re.sub(
            '/gpt', '', content, count=1, flags=re.IGNORECASE)

        if not content.strip():
            return None
        
        try:
            await message.add_reaction(
                self.get_emoji(1057412600696164442))
        except:
            pass

        chat_response = await asyncio.get_running_loop()\
            .run_in_executor(None, _ask_gpt, content)

        if chat_response is None:
            direct_message = await message.author.send(
                f"```\nDigite abaixo sua chave de acesso OpenIA\n```\n"
                f"Caso ainda não tenha uma, crie neste link: "
                f"https://beta.openai.com/account/api-keys"
            )

            await message.channel.send(
                f"Olá {message.author.mention} infelizmente sua chave de "
                f"acesso da OpenIA não está registrada em nosso sistema\n"
                f"Caso queira registrar para acessar o ChatGPT Bot, lhe "
                f"enviei uma mensagem direta com instruções"
            )

            def _check_response(resp: discord.Message) -> bool:
                return (
                    resp.channel.id == direct_message.channel.id
                    and resp.author.id == message.author.id
                )

            try:
                resp: discord.Message = await self.wait_for(
                    "message",
                    check=_check_response,
                    timeout=60*5,
                )

                try:
                    # await asyncio.get_running_loop().run_in_executor(
                    #     None, 
                    #     gpt.insert_api_key, 
                    #     str(resp.author.id), 
                    #     resp.content.strip()
                    # )
                    gpt.insert_api_key(
                        str(resp.author.id), resp.content.strip())

                    await message.author.send("Chave Registrada!")

                except Exception as e:
                    await message.author.send(
                        f"Falha ao registrar Chave: {e}")

            finally:
                return None

        if type(chat_response) is str and len(chat_response) > 2000:
            chat_response = f"{chat_response[:1995]}\n..."

        await message.channel.send(chat_response)
        await message.clear_reactions()
