#meta developer: @confuseeeed, @xeliksm
from .. import loader, utils
from telethon import TelegramClient
from telethon.tl.patched import Message
from telethon.tl.types import ChatBannedRights
from telethon.tl.functions.channels import EditBannedRequest


@loader.tds
class BanAutoMod(loader.Module):
    """BanAuto"""
    strings = {'name': 'BanAuto'}

    async def client_ready(self, client: TelegramClient, db):
        self.client = client
        self.db = db

    async def banautocmd(self, message: Message):
        """Добавить или исключить человека из автобана. .banauto<ник или реплай>"""
        users = self.db.get("BanAuto", "users", [])
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        if not (args or reply):
            return await message.edit("Нету аргументов или реплая")

        if args == "list":
            if not users:
                return await message.edit("Нету людей")

            msg = ""
            for _ in users:
                try:
                    user = await self.client.get_entity(_)
                    msg += f"• <a href=\"tg://user?id={user.id}\">{user.first_name}</a>\n"
                except:
                    users.remove(_)
                    self.db.set("BanAuto", "users", users)
                    return await message.edit("Ошибка,напиши заново команду")

            return await message.edit(f"Список людей в бане:\n\n{msg}")

        try:
            user = await self.client.get_entity(reply.sender_id if reply else args if not args.isnumeric() else int(args))
        except ValueError:
            return await message.edit("Не могу найти чела")

        if user.id not in users:
            users.append(user.id)
            text = "добавлен"
        else:
            users.remove(user.id)
            text = "удален"

        self.db.set("BanAuto", "users", users)
        await message.edit(f"{user.first_name} был {text} в список автобана")


    async def chatautocmd(self, message: Message):
        """Добавить чат в список для автоматического бана. .chatauto"""
        chats = self.db.get("BanAuto", "chats", [])
        args = utils.get_args_raw(message)
        chat_id = message.chat_id

        if args == "list":
            if not chats:
                return await message.edit("Нету чатов")

            msg = ""
            for _ in chats:
                try:
                    chat = await self.client.get_entity(_)
                    msg += f"• {chat.title} | {chat.id}\n"
                except:
                    chats.remove(_)
                    self.db.set("BanAuto", "users", chats)
                    return await message.edit("Ошибка,напиши заново ошибку")

            return await message.edit(f"Список чатов для авто бана:\n\n{msg}")

        if message.is_private:
            return await message.edit("Не чат")

        if chat_id not in chats:
            chats.append(chat_id)
            text = "добавлен в"
        else:
            chats.remove(chat_id)
            text = "удален из"

        self.db.set("BanAuto", "chats", chats)
        return await message.edit(f"Этот чат был {text} списка чатов для автобана")


    async def watcher(self, message: Message):
        try:
            users = self.db.get("BanAuto", "users", [])
            chats = self.db.get("BanAuto", "chats", [])
            user = message.sender
            chat_id = message.chat_id

            if chat_id not in chats:
                return

            if user.id in users:
                for _ in chats:
                    try:
                        await self.client(
                            EditBannedRequest(
                                _, user.id, ChatBannedRights(
                                    until_date=None, view_messages=True
                                )
                            )
                        )
                    except: pass
                return await message.respond(f"{user.first_name} был забанен")
        except:
            pass
