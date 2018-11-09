import unittest
from unittest.mock import patch
from app import *
from config import TestingConfig


class ChallengeTestCase(unittest.TestCase):

    def setUp(self):
        app.config.from_object(TestingConfig)
        db.create_all()

        self.fake_queue = patch('routes.translation_queue')
        self.fake_queue.start()

    def tearDown(self):
        self.fake_queue.stop()
        db.session.remove()
        db.drop_all()

    def test_home_status_code(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_route_works_as_expected(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertIn(b'Unbabel Backend Challenge', response.data)

    def test_home_post_translation(self):
        tester = app.test_client(self)
        data = {'text': 'Hello'}
        response = tester.post('/', data=data)
        self.assertEqual(response.status_code, 302)

    def test_home_get_translation(self):
        translation = Translator(text='Testing', uid='123456789', status='requested')
        db.session.add(translation)
        db.session.commit()
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertIn(b'Testing', response.data)

    def test_home_get_translation_done(self):
        translation = Translator(
            text='All right',
            text_translated='Todo bien',
            uid='1234567890',
            status='translated'
        )
        db.session.add(translation)
        db.session.commit()
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertIn(b'Todo bien', response.data)

    @patch('routes.post_translation')
    def test_create_translation(self, mock_uid):
        mock_uid.return_value.uid = '0987654321'
        translation = Translator(text='Hello', status='requested')
        db.session.add(translation)
        db.session.commit()
        create_translation(translation.id, translation.text)
        self.assertEqual(translation.uid, '0987654321')


if __name__ == '__main__':
    unittest.main()
