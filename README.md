
# hearthstone-deck-randomizer
Hearthstone Deck Randomzer is a web app that lets you generate random decks for Hearthstone based on your personal collection.
## Usage
The app gets users collection from the website [Hearthpwn](http://www.hearthpwn.com/). To sync your Hearthstone collection with Hearthpwn I recommend using the program [Innerkeeper](https://www.innkeeper.com/) which does that for you automatically. 
## Installation
Requires django, requests, beautifulsoup 4 and [python-hearthstone](https://github.com/HearthSim/python-hearthstone). These can all be installed by running the command
```
pip install -r requirements.txt
```
To populate the card database you must first get an API key from [Mashape](https://market.mashape.com/). Once you've done that, rename the configexample.ini file to config.ini and open it.
```ini
[Mashape]
mashapekey = yourkeyhere
```
Replace yourkeyhere with the API key you got from Mashape.

To populate the database run the following commands
```
python manage.py updatecards
```
Before you can start the app you must first change the settings in /hearthstone_deck_randomizer/settings.py

Set debug to True and allowed hosts to empty (All hosts are allowed)
```python
DEBUG = True

ALLOWED_HOSTS = []
```
Then start the app by running 
```
python manage.py runserver
```
