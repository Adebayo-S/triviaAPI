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
            current_categories = paginate_endpoints(request, categories)
        except BaseException:
            abort(400)

        if len(current_categories) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "categories": current_categories,
            "total_categories": len(current_categories)
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
        except BaseException:
            abort(400)

        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.all()
        categories = [category.format() for category in categories]

        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(questions),
            "categories": categories,
            "current_category": None
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
            abort(400)

        return jsonify({
            "success": True,
            "deleted": question_id,
            "total_questions": len(questions)
        })

    """
    @TODO:
    An endpoint to handle a POST for a new question,
    which will require the question and answer text,
    category, and difficulty score.

    When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        get_question = body.get('question')
        get_answer = body.get('answer')
        get_category = body.get('category')
        get_difficulty = body.get('difficulty')

        try:
            question = Question(
                question = get_question,
                answer =  get_answer,
                category =  get_category,
                difficulty = get_difficulty
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
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app
