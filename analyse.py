import collections
import json
import emoji

config = json.load(open("config.json"))["analyser"]
FILTER_STANDARD_EMOJI = config["filter_standard_emoji"]
SAMPLE_SIZE = config["sample_size"]

output = json.load(open("output.json"))
valid_emojis = set(output["emojis"])


def considered_emoji(emoji_name):
    if emoji_name not in valid_emojis:
        return False

    if FILTER_STANDARD_EMOJI:
        if emoji.emojize(emoji_name) != emoji_name:
            return False

    return True


def print_report_for_dict(title, emojis, message_count):
    emoji_counts = [
        pair
        for pair in sorted(emojis.items(), key=lambda x: x[1])
        if considered_emoji(pair[0])
    ]
    bottom_n = [name for (name, _) in emoji_counts[:SAMPLE_SIZE]]
    top_n = [name for (name, _) in emoji_counts[-SAMPLE_SIZE:]]
    print(f"{title} ({message_count} messages)")
    print("", f"Top {SAMPLE_SIZE}:", ", ".join(top_n))
    print("", f"Bottom {SAMPLE_SIZE}:", ", ".join(bottom_n))


start_date = output["start_date"]
end_date = output["end_date"]
print(f"Report between {start_date} and {end_date}")

all_emojis = collections.defaultdict(int)
message_count = 0
for channel_name, channel in sorted(output["channels"].items()):
    emojis = channel["emojis"]
    print_report_for_dict("#" + channel_name, emojis, channel["message_count"])
    for emoji_name, count in emojis.items():
        all_emojis[emoji_name] += count
        message_count += count

print_report_for_dict("Total", all_emojis, message_count)
