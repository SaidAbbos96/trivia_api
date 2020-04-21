import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import random

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres:1111@{}/{}".format('localhost:5432', self.database_name)
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
    # We check the issuance of a list of categories.
    def test_get_categories(self):
        # We send a simple Get request without parameters.
        response = self.client().get('/categories')
        # We get as a result of the request.
        data = json.loads(response.data)
        # We save all the results to the corresponding file.
        result_log = "We check the issuance of a list of categories:\nStatus code: " + str(response.status_code) + "\nresult: " + str(data)
        Fout = open( "backend/result_tests/test_get_categories.txt","w" ) 
        Fout.write(result_log)
        Fout.close()
        # Setting and checking the result.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)


    # Check for adding new questions to the database.
    def test_post_new_question(self):
        # We send the data of a new question for recording the database, we select the complexity of the question randomly, and we also select the category randomly.
        post_data = {
            'question': 'New question',
            'answer': 'Answer',
            'difficulty': int(random.randint( 1 , 5 )),
            'category': int(random.randint( 1 , len(Category.query.all()) ))
        }
        # We send a request with data to record a new question in the database.
        response = self.client().post('/questions', json=post_data)
        # We get as a result of the request.
        data = json.loads(response.data)
        # We save all the results to the corresponding file.
        result_log = "We send a request with data to record a new question in the database.:\nStatus code: " + str(response.status_code) + "\nresult: " + str(data)
        Fout = open( "backend/result_tests/test_post_new_question.txt","w" ) 
        Fout.write(str(result_log))
        Fout.close()
        # Setting and checking the result.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)


    # Verify the protection of the write request to the database of empty questions.
    def test_404_post_new_question(self):
        # Send empty data.
        post_data = {
            'question': '',
            'answer': '',
            'category': 1
        }
        response = self.client().post('/questions', json=post_data)
        # We get as a result of the request.
        data = json.loads(response.data)
        # We save all the results to the corresponding file.
        result_log = "Verify the protection of the write request to the database of empty questions.:\nStatus code: " + str(response.status_code) + "\nresult: " + str(data)
        Fout = open( "backend/result_tests/test_404_post_new_question.txt","w" ) 
        Fout.write(str(result_log))
        Fout.close()
        # Setting and checking the result.
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")


    # Testing the removal of individual questions with the click of a button.
    def test_delete_question(self):
        # We get any first question from the database.
        question = Question.query.first()
        # Request removal by clicking the button using the Get method.
        response = self.client().get('/questions/'+ str(question.id))
        # We get as a result of the request.
        data = json.loads(response.data)
        # We save all the results to the corresponding file.
        result_log = "Removing the first question from the database.\nStatus code: " + str(response.status_code) + "\nDeleted: " + str(question.id) + "\nresult: " + str(data) 
        Fout = open( "backend/result_tests/test_delete_question.txt","w" ) 
        Fout.write(str(result_log))
        Fout.close()
        # Setting and checking the result.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
    # Validation of protection regarding a request to remove non-existent problems.
    def test_404_delete_question(self):
        # We get the latest record from the database by identifier.
        question = Question.query.order_by(Question.id.desc()).first()
        # We add + 1 to the identifier of the last database query. To never have such a record.
        # Request removal of a nonexistent question.
        response = self.client().get('/questions/' + str(question.id + 1))
        # We get as a result of the request.
        data = json.loads(response.data)
        # We save all the results to the corresponding file.
        result_log = "Request removal of a nonexistent question.:\nStatus code: " + str(response.status_code) + "\nresult: " + str(data)
        Fout = open( "backend/result_tests/test_404_delete_question.txt","w" ) 
        Fout.write(str(result_log))
        Fout.close()
        # Setting and checking the result.
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")



    # Checking the beginning is a game of random questions.
    def test_post_play_quiz(self):
        # Select a Random category from the database.
        categorie = random.choice(list(map(Category.format, Category.query.all())))
        # Building data to be sent using the post method.
        post_data = {
            'previous_questions': [],
            'quiz_category': {
                'type': categorie['type'],
                'id': categorie['id']
            }
        }
        response = self.client().post('/quizzes', json=post_data)
        data = json.loads(response.data)
        # We save all the results to the corresponding file.
        result_log = "# Checking the beginning is a game of random questions.:\nStatus code: " + str(response.status_code) + "\nresult: " + str(data)
        Fout = open( "backend/result_tests/test_post_play_quiz.txt","w" ) 
        Fout.write(str(result_log))
        Fout.close()
        # Setting and checking the result.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

'''
Sorry to me. that I didn’t write even more tests to test Our applications, but I thought this 6 tests are 
enough to test my knowledge and skills that I mastered in this course
'''


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()