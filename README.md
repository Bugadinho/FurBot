# [FurBot](https://discordapp.com/oauth2/authorize?client_id=746776378510147724&scope=bot)

A cog-based Discord bot with a glorified e621/e926 browser and some fun stuff

## Disclaimer

This bot is my best attempt yet at making a decent Discord bot, but it is nowhere near being perfect, stuff will break and be slow, please be aware of that.

## Requirements

* Python 3.7+
* MySQL Server

## Installation [Linux]

Create a folder for FurBot to reside in and navigate to it

```bash
mkdir furbotDir
cd furbotDir
```

Clone FurBot's repository

```bash
git clone https://github.com/BugadinhoGamers/FurBot.git
```

Add a file named FurBot.json and put the following contents in it, alter configs to your liking

```json
{
    "token" : "PUTYOURDISCORDTOKENHERE",
    "dbuser" : "PUTYOURMYSQLDBUSERNAMEHERE",
    "dbpassword" : "PUTYOURMYSQLDBPASSWORDHERE",
    "dbip" : "PUTYOURMYSQLDBIP",
    "blacklistedCogs" : [
    ],
    "maintainers" : [
	PUTYOURDISCORDINTEGERIDHERE
    ]
}
```

Remember to install the bot's dependencies with pip

```bash
pip install -r FurBot/requirements.txt
```

And finally, to start the bot you do the folowing

```bash
cd FurBot
./bot.py
```

Add the bot to a Discord server and type ``f-help`` in a chat the bot can see to get a command list.

## Contributing
Pull requests are welcome. Just make sure they are compatible and fix/add something relevant

## License
[GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/)