# discord-channel-reaction-probe

Discord enforces a limit on the number of emojis in a server, which often leads to conversations over which emojis to delete.

I present to you an opportunity to be the _winner_ of those conversations with cold, hard data, obtained through the dangerous work of self-botting.

You're on your own if you decide to use this. I disclaim all responsibility.

It might be nice to convert this into a bot that can be invited to servers, so that you can find this information out without Discord sending its agents after you.

## Use

- Install [Poetry](https://python-poetry.org/) on your machine.
- Copy `sample_config.json` to `config.json` and fill in the parameters as appropriate.
- Run `poetry run python probe.py`. This will take some time and crash afterwards (because I don't know how to properly terminate the async loop here, and Python makes me unhappy)
- Once it's done, run `poetry run analyse.py` to get a nice report of the top and bottom-N emoji uses in your server, including both reactions and messages.
