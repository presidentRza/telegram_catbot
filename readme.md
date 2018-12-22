# Telegram Bot

This demo uses python-telegram-bot with python3 to create a simple chatbot with the following features:

### Features

**Ask user for Location**

Only works on smartphone, bot gets lng/lat via GPS (after user clicked on button)


**Let user select one of multiple Options**

Use customized buttons to let user select one from multiple options

**Send image**

Send an image to user user (e.g. a rendered map or a cat image)


## Installation

run install.sh to install library to .local/ with pip3

## Run

App can be run locally with polling or on server (with_webhoks=True)




openssl req -newkey rsa:2048 -sha256 -nodes -keyout YOURPRIVATE.key -x509 -days 365 -out YOURPUBLIC.pem -subj "/C=de/ST=MUNICH/CN=https://telegramcatbott.herokuapp.com/"


### Demo Program

To be found at KreathonBot

**Commands**

- /start
- /help
- /options
- /location
- /cat


## TODO:
- Emoji: https://apps.timwhitlock.info/emoji/tables/unicode
- Inline-Modus
- webhooks with certificates


# Heroku

The app can be deployed on [Heroku](heroku.com):

### Install Heroku

[Setup Heroku for python](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)

https://devcenter.heroku.com/articles/config-varsheroku ps:scale web=0

        