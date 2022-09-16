# Sending anonymous messages to friends

## Starting the bot.

`python main.py`

## Setting up the bot (Read this before trying to use!):
Please make sure to use python3.6, as I cannot guarantee everything will work as expected on older python versions!
This is because markdown parsing is done by iterating through a dict, which are ordered by default in 3.6.

### Configuration

There are two possible ways of configuring your bot: a config.py file.

- `telegram_token`: Your bot token, as a string.
- `lang`: The bot language en/ru

### Python dependencies

Install the necessary python dependencies by moving to the project directory and running:

`pip install -r requirements.txt`.

This will install all necessary python packages.
