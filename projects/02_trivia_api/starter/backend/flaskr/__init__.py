import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)
  #CORS(app, resources={r"*": {"origins": "*"}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response
 
  
  def paginate_lists(request, selection):
    page = request.args.get('page', 1, type=int)
    start =  (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions  
  
  def create_category_dict(categories):
    formatted_categories = [category.format() for category in categories]
    category_keys = []
    category_values = []

    for category in formatted_categories:
      category_keys.append(category['id'])
      category_values.append(category['type'])

    categories_dict = dict(zip(category_keys, category_values))
    return categories_dict
  
  '''
  @TODO-->DONE: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods = ['GET'])
  def get_all_categories():
        """
        Creates a dictionary of all categories
        :return: All categories
        """
        categories = {}
        for category in Category.query.all():
            categories[category.id] = category.type
        return jsonify({
            'categories': categories
        })

  '''
  @TODO-->DONE: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST-->DONE: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def retrieve_questions():
    try:
      questions = Question.query.all()
      formatted_questions = paginate_lists(request, questions)
      categories = Category.query.all()
      categories_dict = create_category_dict(categories)
      return jsonify({
          'success': True,
          'questions': formatted_questions,
          'categories': categories_dict,
          'current_category': None,
          'total_questions': len(questions),
      })
    except Exception as e:
        abort(e.code)
  '''
  @TODO-->DONE: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter(Question.id == question_id).one_or_none()
    
    if question is None:
        abort(422)
    try:
        question.delete()
        return jsonify({
          'success':True
        })

    except:
      abort(400)
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def post_question():
    """
    Adds a question to database
    :return: The question that is added
    """
    
    try:
      question = request.json.get('question')
      answer = request.json.get('answer')
      category = request.json.get('category')
      difficulty = request.json.get('difficulty')
      if not (question and answer and category and difficulty):
          return abort(400,
                        'Required question object keys missing from request '
                        'body')
      question_entry = Question(question, answer, category, difficulty)
      question_entry.insert()
      return jsonify({
          'success': True
          #'question': question_entry.format()
      }), 201
    except:
        abort(422)

      
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 
    
  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions/search', methods=['POST'])
  def search_questions():
    body = request.get_json('search_term')
    search_term = body['search_term']

    if search_term:
        search_results = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
    
    try:
        return jsonify({
                'success': True,
                'questions': [question.format() for question in search_results],
                'total_questions': len(search_results),
                'current_category': None
            })
    except:
      abort(404)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
    category = Category.query.get(category_id)
    category_name = category.type
    
    try:
      questions = Question.query.filter_by(category=category_name).all()  
      if not questions:
          abort(404)
      formatted_questions = [question.format() for question in questions]
      categories = Category.query.all()
      categories_dict = create_category_dict(categories)
      #print (categories_dict)

      return jsonify({
          'success': True,
          'questions': formatted_questions,
          'categories': categories_dict,
          'current_category': category_name, #categories_dict[category_id],
          'total_questions': len(questions),
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    body = request.get_json()
    category_id = body.get('quiz_category').get('id')
    previous_questions = body.get('previous_questions')
    
    


    if ((category is None) or (previous is None)):
        abort(400)

    if (category['id'] == 0):
        questions = Question.query.all()
    else:
        questions = Question.query.filter_by(category=category['id']).all()

    total = len(questions)

    # picks a random question
    def get_random_question(questions):
        return questions[random.randrange(0, len(questions), 1)]

    # checks to see if question has already been used
    def check_if_used(question, previous_questions):
        for q in previous_questions:
            if (q == question.id):
                return True
        return False
    
    found_question = False
    while not found_question:
      # get random question
      question = get_random_question(questions)
      if not check_if_used(question, previous_questions):
          question_to_ask = question
          found_question = True
        break

    try:
      return jsonify({
          'question':question_to_ask
        }), 200
    except:
      abort(422)


  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  @app.after_request
  def bad_request(error):
      return jsonify({
          'success': False,
          'error': 400,
          'message': 'Bad request'
      }), 400

  @app.errorhandler(404)
  @app.after_request
  def not_found(error):
      return jsonify({
          'success': False,
          'error': 404,
          'message': 'Not found'
      }), 404

  @app.errorhandler(405)
  @app.after_request
  def not_allowed(error):
      return jsonify({
          'success': False,
          'error': 405,
          'message': 'Method not allowed'
      }), 405

  @app.errorhandler(422)
  @app.after_request
  def unprocessable(error):
      return jsonify({
          'success': False,
          'error': 422,
          'message': 'Unable to process request'
      }), 422

  @app.errorhandler(500)
  @app.after_request
  def server_error(error):
      return jsonify({
          'success': False,
          'error': 500,
          'message': 'Internal server error'
      }), 500

  return app

    