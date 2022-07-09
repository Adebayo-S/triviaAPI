import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_endpoints(request, selections):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    selections = [selection.format() for selection in selections]
    current_selections = selections[start:end]

    return current_selections


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        try:
            categories = Category.query.all()
            categories_dic = {}

            for category in categories:
                categories_dic[category.id] = category.type
        except BaseException:
            abort(400)

        if len(categories_dic) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "categories": categories_dic,
            "total_categories": len(categories_dic)
        })

    """
    An endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint returns a list of questions,
    number of total questions, current category, categories.
    """

    @app.route('/questions')
    def get_questions():
        try:
            questions = Question.query.all()
            current_questions = paginate_endpoints(request, questions)
            categories = Category.query.all()
            categories_dic = {}

            for category in categories:
                categories_dic[category.id] = category.type
        except BaseException:
            abort(400)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(questions),
            "categories": categories_dic
        })

    """
    An endpoint to handle DELETE question using a question ID.
    When you click the trash icon next to a question, the question will be
    removed.    This removal will persist in the database and when you refresh
    the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()
            questions = Question.query.all()
        except BaseException:
            abort(404)

        return jsonify({
            "success": True,
            "deleted": question_id,
            "total_questions": len(questions)
        })

    """
    An endpoint to handle a POST for a new question,
    which will require the question and answer text,
    category, and difficulty score.

    When you submit a question on the "Add" tab,
    the form will clear and the question will appear
    at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            body = request.get_json()

            get_question = body.get('question')
            get_answer = body.get('answer')
            get_category = body.get('category')
            get_difficulty = body.get('difficulty')

            question = Question(
                question=get_question,
                answer=get_answer,
                category=get_category,
                difficulty=get_difficulty
            )
            question.insert()
            questions = Question.query.all()
        except BaseException:
            abort(400)

        return jsonify({
            "success": True,
            "created": question.id,
            "question": question.question,
            "total_questions": len(questions)
        })

    """
    A POST endpoint to get questions based on a search term.
    It returns any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm')

        try:
            questions = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')
            ).all()
            current_questions = paginate_endpoints(request, questions)
        except BaseException:
            abort(400)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(current_questions)
        })

    """
    A GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category_id(category_id):
        try:
            questions = Question.query.filter(
                Question.category == category_id
            ).all()
            current_questions = paginate_endpoints(request, questions)
            category = Category.query.get(category_id)
        except BaseException:
            abort(404)

        if len(current_questions) == 0 or category is None:
            abort(400)

        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(current_questions),
            "current_category": category.type
        })

    """
    POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=['POST'])
    def get_quiz():
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions')
            category = body.get('quiz_category')

            if category['id'] == 0:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)
                ).all()
            else:
                questions = Question.query.filter(
                    Question.category == category['id'],
                    Question.id.notin_(previous_questions)
                ).all()
            randm_question = random.choice(
                questions) if len(questions) > 0 else None
        except BaseException:
            abort(422)

        return jsonify({
            "success": True,
            "question": randm_question.format()
        })

    """
    Error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "server error"
        }), 500

    return app
