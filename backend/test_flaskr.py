import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category
from models import DB_USER, DB_PASSWORD, DB_HOST

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            DB_USER, DB_PASSWORD, DB_HOST, self.database_name
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        """
        Test get_categories endpoint to get the categories
        """
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(data['categories'])

    def test_get_questions(self):
        """
        Test get_questions endpoint to get the questions
        """
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])

    def test_delete_question(self):
        """
        Test delete_question endpoint to delete a question
        """
        question = Question(
            question='did this test pass?',
            answer='yes',
            category=1,
            difficulty=1
        )
        question.insert()
        question_id = str(question.id)
        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_add_question(self):
        """
        Test add_question endpoint to add a question
        """
        res = self.client().post('/questions', json={
            'question': 'did I add this question?',
            'answer': 'yes',
            'category': 1,
            'difficulty': 1
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_search_questions(self):
        """
        Test search_questions endpoint to return results
        for search questions
        """
        url = '/questions/search'
        res = self.client().post(url, json={
            'searchTerm': 'autobiography'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_get_quiz(self):
        """
        Test get_quiz endpoint to return quiz data
        """
        url = '/quizzes'
        res = self.client().post(url, json={
            'quiz_category': {"type": "Science", "id": "1"},
            'previous_questions': []
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
