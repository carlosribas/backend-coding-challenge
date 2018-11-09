import unittest
from unittest.mock import patch
from app import *
from config import TestingConfig


class ChallengeTestCase(unittest.TestCase):

    def setUp(self):
        app.config.from_object(TestingConfig)
        db.create_all()

        self.fake_queue = patch('main.routes.translation_queue')
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
        self.assertEqual(translation.__repr__(), "<Text " + "'" + translation.text + "'>")

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

    @patch('main.routes.post_translation')
    def test_create_translation(self, mock_uid):
        mock_uid.return_value.uid = '0987654321'
        translation = Translator(text='Hello', status='requested')
        db.session.add(translation)
        db.session.commit()
        create_translation(translation.id, translation.text)
        self.assertEqual(translation.uid, '0987654321')

    @patch('main.routes.get_translation')
    @patch('time.sleep')
    def test_update_translation_completed(self, mock_time, mock_get_translation):
        mock_time.return_value = None
        mock_get_translation.return_value.status = 'completed'
        mock_get_translation.return_value.translation = 'Muy inteligente'
        translation = Translator(text='Very clever', status='pending', uid='5678901234')
        db.session.add(translation)
        db.session.commit()
        update_translation(translation.id)
        self.assertEqual(translation.status, 'translated')
        self.assertIsNotNone(translation.text_translated)


if __name__ == '__main__':
    unittest.main()
