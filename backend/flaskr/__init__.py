# Import the necessary components.
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

# Import settings and database connections.
from models import setup_db, Question, Category


# The number of questions per page.
QUESTIONS_PER_PAGE = 10

# Function controller questions per page.
def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions


  
# The main function of the entire application.
def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  # Base route to test whether our server is running.
  @app.route("/")
  def home():
      num = "Hi ! I`m SaidAbbos.<br> abbos.xudoyqulov@gmail.com"
      return str(num)
  # Configuring cors after request completion.
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  # Access Controller and advanced options.
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response

  # Controller list of categories.
  @app.route("/categories", methods=['GET'])
  def get_categories():
      # Getting a list of categories from a database.
      categories = list(map(Category.format, Category.query.all()))
      # Another way to build a list of categories is if additional parameters are required.
      # categories = []
      # for cat in Category.query.all():
      #   data = {
      #     "id": cat.id, 
      #     "type": cat.type
      #   }
      #   categories.append(data)
      
      # Check If the category is missing, return an error. 
      if (len(categories) == 0):
          abort(404)
      # Build the result of Json format.
      result = {
          "success": True,
          "categories": categories
      }
      # return result
      return jsonify(result)


  # Controller list of questions.
  @app.route('/questions')
  def get_questions():
    # We get all the questions in reverse order by identifier.
    selection = Question.query.order_by(Question.id.desc()).all()
    # Check the limit of questions in one page.
    current_questions = paginate_questions(request, selection)
    # getting a list of categories and counter issues
    categories = []
    for cat in Category.query.all():
      data = {
        "counter": len(Question.query.filter(Question.category == cat.id).all()),
        "id": cat.id, 
        "type": cat.type
      }
      categories.append(data)
    # If there are no questions left after the limit, we return an error.If there are no questions left after the limit, we return an error.
    if len(current_questions) == 0:
      abort(404)

    # Build the result of Json format.
    list_questions = {
      'success': True,
      'questions': current_questions,
      'total_questions': len(Question.query.all()),
      'categories': categories,
      'current_category': None,
    }
    # return result
    return jsonify(list_questions)


  # Removing questions from the database by a unique identifier.
  @app.route('/questions/<int:question_id>', methods=['GET'])
  def delete_question(question_id):
      # We are looking for a question from the database by identifier.
      question = Question.query.filter(Question.id == question_id).one_or_none()
      #If the program does not find such a question with such an identifier, an error is returned.
      if question is None:
        abort(404)
      #Delete the found question.
      question.delete()
      # After successful removal, we return the remaining list of questions.
      selection = Question.query.order_by(Question.id.desc()).all()
      # Check the limit of questions on one page.
      current_questions = paginate_questions(request, selection)
      # construction of the returned result, inside the result, information about the removal and the list of remaining questions
      result_deleted = {
        'success': True,
        'deleted': question_id,
        'questions': current_questions,
        'total_questions': len(Question.query.all())
      }
      
      return jsonify(result_deleted)


  # Controller creating new questions using the Post method.
  @app.route("/questions", methods=['POST'])
  def add_question():
    # we receive data from the form
    data = request.get_json()

    new_question = data.get('question', None)
    new_answer = data.get('answer', None)
    new_category = data.get('category', None)
    new_difficulty = data.get('difficulty', None)
    # Blank write protection.
    if (len(new_question) < 5) or (len(new_answer) < 5) or (new_category is None):
      abort(404)
    # We fill in all the data and save a new question.
    new_question = Question(question=new_question,answer=new_answer, category=new_category, difficulty=new_difficulty)
    new_question.insert()
    return jsonify({
      'success': True,
    })


  # Questions Search Controller.
  @app.route("/QuestionsSearch", methods=['POST'])
  def search_questions():
      # Check if the keys to search if not, return an error.
      if request.data:
          # We receive data in json format.
          data = request.get_json()
          # get the key to search
          term = data.get('searchTerm', None)
          # Check if the key length is less than 3 characters, return an error.
          if len(term) < 3:
            abort(404)
          else:
            # If all is well search questions from the database by key.
            # We look for all the questions from the database that contain such a key and sort the reverse order by identifier
            # We are looking for questions, regardless of case.
            res = Question.query.filter(Question.question.ilike('%' + term + '%')).order_by(Question.id.desc()).all()
            # If we do not find a single question then we return an error.
            if (len(res) == 0):
              abort(404)
            # We develop a list of questions on one page.
            questions = paginate_questions(request, res)
            # Building a search result of questions.
            result = {
                "success": True,
                "questions": questions,
                "total_questions": len(res),
                "current_category": None,
            }
            # return status and result
          return jsonify(result)
      abort(404)
      

  # The controller of all questions in a certain category.
  @app.route("/categories/<int:category_id>/questions")
  # we get the variables and the link
  def get_question_by_category(category_id):
      # We get a list of categories.
      categories = list(map(Category.format, Category.query.all()))
      # We get the data of the selected category.
      category_data = Category.query.get(category_id)
      # We get all the questions for the selected category.The result is returned by sorting by identifier in reverse order.
      questions_query = Question.query.filter_by(category=category_id).order_by(Question.id.desc()).all()
      # We develop a list of questions on one page.
      questions = paginate_questions(request, questions_query)
      # After the limit, we check whether there are questions, return the result.
      # If there are no questions left, we return an error.
      if len(questions) > 0:
          result = {
              "success": True,
              "questions": questions,
              "total_questions": len(questions_query),
              "categories": categories,
              "current_category": Category.format(category_data),
          }
          return jsonify(result)
      abort(404)

# Controller random questions for the selected category.
  @app.route("/quizzes", methods=['POST'])
  def play_question_quiz():
    # Check the existence request.
      if request.data:
        # If the request is not empty then we get data from json.
          data = request.get_json()
          #getting the identifier of the selected category. If no category is selected, then randomly return from the list of categories 
          category_id = int(data["quiz_category"]["id"])
          if category_id == 0:
              category_id = random.randint( 1 , len(Category.query.all()) )

          # we get all questions from the database for the selected category. which is not selected before
          questions = Question.query.filter_by(category=category_id).filter(Question.id.notin_(data["previous_questions"])).all()
          # Check if there are questions, then return a random question from the list.
          count = len(questions)
          if count > 0:
              result = {
                      "success": True,
                      "question": Question.format(questions[random.randrange(0,count)])
                  }
          # If no questions are found, return the status and an empty result.
          else:
              result = {
                      "success": True,
                      "question": None
                  }
          return jsonify(result)
      abort(422)
# _________________________________________________
# In case of an error, return the error code and text.

# if the program understands the request but cannot process it. then return the error code
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
    }), 422
# If the program does not find the requested resource, then return.
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Resource not found"
    }), 404

  return app

    