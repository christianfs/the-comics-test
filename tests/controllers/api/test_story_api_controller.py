import unittest
import pytest
import src.controllers.api.story_api_controller as story_api_controller

from werkzeug.exceptions import NotFound
from unittest.mock import patch
from faker import Faker
from src.controllers.story_controller import StoryController

class TestStoryApiController(unittest.TestCase):

    def setUp(self):
        self.fake = Faker()

    @patch.object(StoryController, 'get_character_story')
    def test_get_character_story_with_story_should_return_character_story(self, mock_get_character_story):
        character_story = self.fake.text(max_nb_chars=200)
        mock_get_character_story.return_value = character_story
        story = story_api_controller.get_character_story(self.fake.pyint())
        self.assertEqual(story, character_story)

    @patch.object(StoryController, 'get_character_story')
    def test_get_character_story_empty_story_should_return_404(self, mock_get_character_story):
        character_id = self.fake.pyint()
        mock_get_character_story.return_value = None
        with pytest.raises(NotFound) as e:
            story_api_controller.get_character_story(character_id)
        assert str(e.value) == '404 Not Found: Character with ID {} not found'.format(character_id)
