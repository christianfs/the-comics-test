import unittest
import json

from faker import Faker
from src.services.story_service import StoryService, HTTP_STATUS_OK
from src.controllers.story_controller import StoryController
from unittest.mock import patch


class TestStoryController(unittest.TestCase):

    def setUp(self):
        self.fake = Faker()
        self.story_controller = StoryController()

    def test_get_random_story_with_stories_should_return_story(self):
        stories = self.fake.pylist(nb_elements=5, variable_nb_elements=True, value_types=['str'])
        response = self.story_controller.get_random_story(stories)
        self.assertIn(response, stories)

    def test_get_random_story_empty_stories_should_return_none(self):
        stub_stories = []
        response = self.story_controller.get_random_story(stub_stories)
        self.assertIsNone(response)

    @patch.object(StoryController, 'get_random_story')
    @patch.object(StoryController, 'get_story_characters_information')
    def test_get_story_info_with_story_should_return_story_info(self, mock_get_story_characters_information, mock_get_random_story):
        expected_result = {
            'title': 'Test',
            'description': 'Description',
            'characters': [{'imageUrl': 'caminho/imagem.jpg', 'name': 'Image'}],
            'attribution': 'MARVEL'
        }
        mock_get_random_story.return_value = json.loads('{ "title": "Test", "description": "Description", "resourceURI":"ResourceUri" }')
        mock_get_story_characters_information.return_value = ([json.loads('{ "imageUrl": "caminho/imagem.jpg", "name": "Image" }')], HTTP_STATUS_OK)
        response = self.story_controller.get_story_info(json.loads('{ "attributionText":"MARVEL", "data":{ "results":[ { } ] } }'))
        self.assertEqual(response, expected_result)

    @patch.object(StoryController, 'get_random_story')
    @patch.object(StoryController, 'get_story_characters_information')
    def test_get_story_info_with_empty_story_should_return_none(self, mock_get_story_characters_information, mock_get_random_story):
        expected_result = {
            'title': 'Test',
            'description': 'Description',
            'characters': [{'imageUrl': 'caminho/imagem.jpg', 'name': 'Image'}],
            'attribution': 'MARVEL'
        }
        mock_get_random_story.return_value = None
        response = self.story_controller.get_story_info(json.loads('{ "attributionText":"MARVEL", "data":{ "results":[ { } ] } }'))
        self.assertIsNone(response)

    @patch.object(StoryService, 'get_story_characters_information')
    def test_get_story_characters_information_should_return_characters_information(self, mock_get_story_characters_information):
        mock_story_server_response = ('{'
            '"data":{'
                '"results":['
                    '{'
                        '"name":"Beast",'
                        '"thumbnail":{'
                            '"path":"http://i.annihil.us/u/prod/marvel/i/mg/2/80/511a79a0451a3",'
                            '"extension":"jpg"'
                        '}'
                    '},'
                    '{'
                        '"name":"Captain America",'
                        '"thumbnail":{'
                            '"path":"http://i.annihil.us/u/prod/marvel/i/mg/3/50/537ba56d31087",'
                            '"extension":"jpg"'
                        '}'
                    '},'
                    '{'
                        '"name":"Cyclops",'
                        '"thumbnail":{'
                            '"path":"http://i.annihil.us/u/prod/marvel/i/mg/6/70/526547e2d90ad",'
                            '"extension":"jpg"'
                        '}'
                    '}'
                ']'
            '}'
        '}')
        expected_result = (
            [{
                'imageUrl': 'http://i.annihil.us/u/prod/marvel/i/mg/2/80/511a79a0451a3/portrait_medium.jpg',
                'name': 'Beast'
            },
            {
                'imageUrl': 'http://i.annihil.us/u/prod/marvel/i/mg/3/50/537ba56d31087/portrait_medium.jpg',
                'name': 'Captain America'
            },
            {
                'imageUrl': 'http://i.annihil.us/u/prod/marvel/i/mg/6/70/526547e2d90ad/portrait_medium.jpg',
                'name': 'Cyclops'
            }]
        )
        mock_get_story_characters_information.return_value = (json.loads(mock_story_server_response), HTTP_STATUS_OK)
        characters, http_status_code = self.story_controller.get_story_characters_information('http://gateway.marvel.com/v1/public/stories/670')
        self.assertEqual(characters, expected_result)
        self.assertEqual(http_status_code, HTTP_STATUS_OK)

    @patch.object(StoryService, 'get_story_characters_information')
    def test_get_story_characters_information_without_story_characters_information_should_return_none_and_http_status_ok(self, mock_get_story_characters_information):
        mock_get_story_characters_information.return_value = (None, HTTP_STATUS_OK)
        characters, http_status_code = self.story_controller.get_story_characters_information('http://gateway.marvel.com/v1/public/stories/670')
        self.assertIsNone(characters)
        self.assertEqual(http_status_code, HTTP_STATUS_OK)

    @patch.object(StoryController, 'get_story_info')
    @patch.object(StoryService, 'get_character_story')
    def test_get_character_story_should_return_character_story(self, mock_get_character_story, mock_get_story_info):
        expected_story_info = {
            'title': 'Test',
            'description': 'Description',
            'characters': [{'imageUrl': 'caminho/imagem.jpg', 'name': 'Image'}],
            'attribution': 'MARVEL'
        }
        mock_get_character_story.return_value = (json.loads('{ "data": { "results": [ { "title": "Test", "description": "Description", "resourceURI":"ResourceUri" }]}}'), HTTP_STATUS_OK)
        mock_get_story_info.return_value = expected_story_info
        response, http_status_code = self.story_controller.get_character_story("1009220")
        self.assertEqual(response, expected_story_info)
        self.assertEqual(http_status_code, HTTP_STATUS_OK)

    @patch.object(StoryService, 'get_character_story')
    def test_get_character_story_without_character_story_should_return_none_and_http_status_ok(self, mock_get_character_story):
        mock_get_character_story.return_value = (None, HTTP_STATUS_OK)
        response, http_status_code = self.story_controller.get_character_story("1009220")
        self.assertIsNone(response)
        self.assertEqual(http_status_code, HTTP_STATUS_OK)
