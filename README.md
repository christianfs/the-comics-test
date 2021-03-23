## The Comics Test
This project consists of showing information about a random Marvel story throughout by a **character id**.

## Motivation
Project created to satisfied **The Comics Test** challenge.

## Tech/framework used

<b>Built with</b>
- [Python 3.8.5](https://www.python.org/downloads/release/python-385/)
- [Flask 1.1.2](https://flask.palletsprojects.com/en/1.1.x/)

## Features
Using the [Marvel API](http://developer.marvel.com/docs), a random story featuring a character is shown in a generated HTML page
with the following characteristics:

 - The story's description
 - A list of names and pictures of the characters that feature in the story
 - The Marvel attribution text

## Installation
In a terminal in your development env is necessary to run:

- pip install -r requirements.txt (to install all requirements to this project)

## Tests
Run **./test.sh** in a terminal.

## How to use?

- You need to add two environment variables, you are allowed to use the .env file to simulate in your machine:
    - MARVEL_PUBLIC_KEY
    - MARVEL_PRIVATE_KEY 
- Run **./run.sh** in a terminal.
- In the development environment, access the URI **http://0.0.0.0:5000/?characterId=<character_id>**, if you do not provide the character_id the app will use Captain America's Id. You can search the ids in the [Marvel public API](https://developer.marvel.com/docs#!/public/)