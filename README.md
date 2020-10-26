# FurBot

A glorified e621/e926 browser for Discord with some fun stuff

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

To start up the bot, just do the following

```bash
cd FurBot
./bot.py
```

Add the bot to a Discord server and type ``f-help`` in a chat the bot can see to get a command list.

## Contributing
Pull requests are welcome. Just make sure they are compatible and fix/add something relevant

## License
[GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/)