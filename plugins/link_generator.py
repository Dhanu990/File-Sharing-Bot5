@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    def get_valid_message(prompt):
        while True:
            try:
                response = await client.ask(text=prompt, chat_id=message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
            except:
                return None
            msg_id = await get_message_id(client, response)
            if msg_id:
                return response, msg_id
            else:
                await response.reply("❌ Error: This message is not from the DB Channel or the link is not valid", quote=True)

    first_message, f_msg_id = get_valid_message("Forward the First Message from DB Channel (with Quotes) or Send the DB Channel Post Link")
    if not first_message:
        return

    second_message, s_msg_id = get_valid_message("Forward the Last Message from DB Channel (with Quotes) or Send the DB Channel Post link")
    if not second_message:
        return

    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await second_message.reply_text(f"<b>Here is your link</b>\n\n{link}", quote=True, reply_markup=reply_markup)

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    channel_message, msg_id = get_valid_message("Forward Message from the DB Channel (with Quotes) or Send the DB Channel Post link")
    if not channel_message:
        return

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await channel_message.reply_text(f"<b>Here is your link</b>\n\n{link}", quote=True, reply_markup=reply_markup)
