# Discord REPL

A discord bot to run code in containers.

---

## Development

Requirements

- python 3.10
- docker

---

Install pipenv

```sh
python -m pip install --user pipenv
```

---

Prepare the environment

```sh
pipenv install --dev
```

---

Run the tests

```sh
pipenv run test
```

---

## Running the bot

First of all you will need to create a application/bot on discord. Here are some usefully links:

- <https://discord.com/developers/docs/intro>
- <https://discord.com/developers/applications>

Get your bot token and add it to `.env` or as variable when running the bot.

---

Using `.env`.

Add to the `.env`

```sh
echo "DISCORD_TOKEN=... >> .env
```

Run the bot

```sh
pipenv run bot
```

Take care of your token, don't commit it.

---

Using as variable

```sh
DISCORD_TOKEN=... pipenv run bot
```
