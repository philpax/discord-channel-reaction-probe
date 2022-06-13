import collections
from datetime import datetime, timedelta
import itertools
import discord
import json
import re
import emoji


client = discord.Client(
    guild_subscription_options=discord.GuildSubscriptionOptions.off()
)

config = json.load(open("config.json"))["probe"]
GUILD_ID = config["guild_id"]
TOKEN = config["token"]
END_DATE = datetime.now()
START_DATE = END_DATE - timedelta(weeks=config["week_count"])


def extract_emojis_from_string(s):
    return re.findall(r":[A-z0-9]+:", emoji.demojize(s))


@client.event
async def on_ready():
    print("Logged on as", client.user)
    print(f"Scraping from {START_DATE.isoformat()} to {END_DATE.isoformat()}")

    guild = client.get_guild(int(GUILD_ID))
    supported_channels = [
        channel
        for channel in guild.channels
        if isinstance(channel, discord.TextChannel)
    ]

    channels_counts = {}
    for channel in supported_channels:
        if channel.permissions_for(guild.me).read_message_history:
            channel_counts = collections.defaultdict(int)
            message_count = 0
            async for message in channel.history(
                after=START_DATE, before=END_DATE, limit=None
            ):
                for emoji in itertools.chain(
                    extract_emojis_from_string(message.content),
                    *[
                        extract_emojis_from_string(str(reaction))
                        for reaction in message.reactions
                    ],
                ):
                    channel_counts[emoji] += 1
                message_count += 1
            channels_counts[str(channel)] = {
                "emojis": channel_counts,
                "message_count": message_count,
            }

    json.dump(
        {
            "channels": channels_counts,
            "emojis": list(
                itertools.chain(
                    *[extract_emojis_from_string(str(emoji)) for emoji in guild.emojis]
                )
            ),
            "start_date": START_DATE.isoformat(),
            "end_date": END_DATE.isoformat(),
        },
        open("output.json", "w"),
    )

    print("Done!")

    await client.close()


client.run(TOKEN)
