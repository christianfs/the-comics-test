import hashlib
import requests
import json
import src.config as config

from datetime import datetime


HTTP_STATUS_OK = 200
HTTP_STATUS_SERVER_ERROR = 500

class StoryService:
    def __init__(self):
        self.marvel_public_key = config.marvel_public_key
        self.marvel_private_key = config.marvel_private_key
        self.params = {'ts': self.__get_timestamp(), 'apikey': self.marvel_public_key, 'hash': self.__hash_params()}

    def __get_timestamp(self):
        return datetime.now().strftime(("%Y-%m-%d%H:%M:%S"))

    def __hash_params(self):
        self.hash_md5 = hashlib.md5()
        self.timestamp = self.__get_timestamp()
        self.hash_md5.update(f'{self.timestamp}{self.marvel_private_key}{self.marvel_public_key}'.encode('utf-8'))
        self.hashed_params = self.hash_md5.hexdigest()
        return self.hashed_params

    def get_character_story(self, characterId):
        self.story = None
        try:
            self.res = requests.get('http://gateway.marvel.com/v1/public/characters/{characterId}/stories'.format(characterId=characterId),
                        params=self.params)
        except:
            return self.story, HTTP_STATUS_SERVER_ERROR
        if self.res.status_code == HTTP_STATUS_OK:
            self.story = json.loads(self.res.text)
        return self.story, self.res.status_code

    def get_story_characters_information(self, story_uri):
        self.story_characters = None
        try:
            self.res = requests.get('{}/characters'.format(story_uri), params=self.params)
        except:
            return self.story_characters, HTTP_STATUS_SERVER_ERROR
        if self.res.status_code == HTTP_STATUS_OK:
            self.story_characters = json.loads(self.res.text)
        return self.story_characters, self.res.status_code
