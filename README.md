# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.

<br>
<br>

# API Documentation

## Running the server

> In the `backend` directory and in a virtial environment, run the server:

- command prompt

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development

flask run
```

- powershell

```bash
$env:FLASK_APP="flaskr"
$env:FLASK_ENV="development"

python -m flask run
```

## Running the Frontend in Dev Mode

> The `frontend` directory contains the React frontend files used.

run the following command to isntall dependencies and to start the react-app locally.

```bash
npm install
npm start
```

## Endpoints

### GET /categories

Request: `GET`

> Fetches all questions and returns a json list of paginated categories.

Example: ```curl http://localhost:5000/categories```

Response body

```json
{
    "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "success": true,
  "total_categories": 6
}
```

### POST /questions

Request: `POST`

> Creates a new question object and returns a json response containing the id of the created question and the total number of questions.

Example: ```curl -X POST -H 'Content-Type: application/json' -d '{"question": "test question 1", "answer": "pass", "category": 1, "difficulty": 1}' http://127.0.0.1:5000/questions```

Response:

```json
{
    "created": 24,
    "question": "test question 1",
    "success": true,
    "total_questions": 20
}
```

### DELETE /questions/<question_id>

Request: `DELETE`

> Deletes a question object of `id: question_id` from the database.
On success, it returns the id of the deleted question message and number of questions remaining.

Example: ```curl -X DELETE http://localhost:5000/questions/24```

Response:

```json
{
    "deleted": 24,
    "success": true,
    "total_questions": 19
}
```

### GET /questions

Request: `GET`

> Fetches all questions and returns a json list of paginated questions.

Example: ```curl http://localhost:5000/questions```

Response:

```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
        {
            "answer": "Colorado, New Mexico, Arizona, Utah",
            "category": 3,
            "difficulty": 3,
            "id": 164,
            "question": "Which four states make up the 4 Corners region of the US?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "success": true,
    "total_questions": 19
}
```

### GET /categories/<category_id>/questions

Request: `GET`

> Request that gets the questions based on the category_id and returns the json object of paginated questions.

Example: ```curl http://localhost:5000/categories/4/questions```

Response:

```json
{
  "current_category": "History",
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ],
  "success": true,
  "total_questions": 4
}
```

### POST /quizzes

Request: `POST`

> The request is made with the category id to fetch a random question from the given category that is not amongst the previous categories.

```json
data = {
    "previous_questions": [],
    "category_id": 1
}
```

Example: ```curl -X POST http://localhost:5000/quizzes -d '{"previous_questions": [], "quiz_category": {"type": "Science", "id": "1"}}'```

Response:

```json
{
  "question": {
    "answer": "Blood",
    "category": 1,
    "difficulty": 4,
    "id": 22,
    "question": "Hematology is a branch of medicine involving the study of what?"
  },
  "success": true
}

```

### POST / questions/search

Request: `POST`

> A POST request is made with search term as a json data and it fetches all questions with search term as a substring in the question and returns a json response of all questions.

Example: ``` curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "autobiography"}' ```

Response:

```json
{
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

## Error Handling

> When an exception is thrown, a json object in the format below is returned:

Response:

```json
{
    "success": False,
    "error": <error code>,
    "message": "<error message>"
}
```

where:

- 400: Bad request
- 404: Resource not Found
- 422: Unprocessable Entity


## Testing

> Running tests for the projects.

```bash

dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py

```

## Author

Adebayo Samuel @Adebayo-S
