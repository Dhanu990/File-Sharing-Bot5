@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    try:
        channel_messages = []
        while True:
            try:
                channel_message = await client.ask(
                    text="Forward Message(s) or Send Post link(s) separated by spaces",
                    chat_id=message.from_user.id,
                    filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                    timeout=60
                )
                channel_messages.append(channel_message)
            except:
                if not channel_messages:
                    await message.reply("❌ Error: Couldn't get any valid messages. Please try again.")
                break

        if not channel_messages:
            return

        links = []
        for channel_message in channel_messages:
            msg_id = await get_message_id(client, channel_message)
            if msg_id:
                base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
                link = f"https://t.me/{client.username}?start={base64_string}"
                links.append(link)
            else:
                await channel_message.reply(f"❌ Error: Invalid Post Link or Message - {channel_message.link}", quote=True)

        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}') for link in links]
        ])

        formatted_links = "\n".join(links)

        await message.reply_text(f"<b>Here are your links:</b>\n\n{formatted_links}", quote=True, reply_markup=reply_markup)
        await message.reply("✅ Links generated successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
