from flask import abort
from src.controllers.story_controller import StoryController


STORY_CONTROLLER = StoryController()

def get_character_story(characterId):
    story = STORY_CONTROLLER.get_character_story(characterId)
    if story:
        return story
    else:
        abort(
            404, "Character with ID {characterId} not found".format(characterId=characterId)
        )
