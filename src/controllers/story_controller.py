import random

from src.services.story_service import HTTP_STATUS_OK, StoryService

PORTRAIT_SIZE = 'portrait_medium'

class StoryController:
    def __init__(self):
        self.story_service = StoryService()

    def get_random_story(self, stories):
            self.searching_story = True
            self.story_size = len(stories)

            if self.story_size == 0:
                return None

            self.story = None
            idx = random.randint(0, self.story_size-1)
            self.story = stories[idx]
            self.searching_story = False
            return self.story

    def get_story_info(self, story):
        self.random_story = self.get_random_story(story['data']['results'])

        if self.random_story is None:
            return None

        self.characters, self.http_status_code = self.get_story_characters_information(self.random_story['resourceURI'])
        res = {
            'title': self.random_story['title'],
            'description': self.random_story['description'],
            'characters': self.characters,
            'attribution': story['attributionText']
        }
        return res

    def get_story_characters_information(self, story_uri):
        self.story_characters_information, self.http_status_code = self.story_service.get_story_characters_information(story_uri)
        
        if not self.story_characters_information or not self.story_characters_information['data']['results']:
            return None, self.http_status_code

        self.res = []
        for character in self.story_characters_information['data']['results']:
            thumbnail_path = character['thumbnail']['path']
            thumbnail_extension = character['thumbnail']['extension']
            self.res.append({ 
                'imageUrl': '{}/{}.{}'.format(thumbnail_path, PORTRAIT_SIZE, thumbnail_extension), 
                'name': character['name']
            })
        return self.res, HTTP_STATUS_OK

    def get_character_story(self, characterId):
        self.story, self.http_status_code = self.story_service.get_character_story(characterId)

        if not self.story or not self.story['data']['results']:
            return None, self.http_status_code
        self.story_info = self.get_story_info(self.story)
        return self.story_info, HTTP_STATUS_OK
