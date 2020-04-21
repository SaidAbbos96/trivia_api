# Full Stack Trivia API Project
---------------------------------
## Full Stack Trivia

This project is a game where users can test their knowledge answering trivia questions. The task for the project was to create an API and test suite for implementing the following functionality:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 


## Getting Started

### Installing Dependencies
Developers using this project should already have Python3, pip, node, and npm installed.

#### Frontend Dependencies

This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

#### Backend Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

## Running the Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```


## Running the Server

From within the `backend` directory first ensure you are working using your created virtual environment.

### Running a program through the console using a bash program or on a unix Linux macos platform:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

###Running the program on a Windows powershell program on a Windows platform.

```Windows PowerShell
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
### All test results are saved with the appropriate name in the folder.
folder for test results files:
```backend\result_tests```

"Omit the dropdb command the first time you run tests."


## API Reference

### Getting Started

* Base URL: Currently this application is only hosted locally. The backend is hosted at `http://127.0.0.1:5000/`
* Authentication: This version does not require authentication or API keys.


### Error Handling

Errors are returned as JSON in the following format:<br>

    {
        "success": False,
        "error": 404,
        "message": "resource not found"
    }

The API will return three types of errors:

* 404 – resource not found
* 422 – unprocessable


### Endpoints

#### GET /categories

* General: Returns a list categories.
* Sample: `curl http://127.0.0.1:5000/categories`<br>

        {
            "categories": {
                [
		 "id", // Unique identifier for a category.
		 "type" // Name of category
		],
		.... // Displays all categories.
            }, 
            "success": true // The status of the request, if the result is always the value true.
        }



#### GET /questions

* General:
  * Returns a list questions.
  * Results are paginated in groups of 10.
  * Also returns list of categories and total number of questions.
* Sample: `curl http://127.0.0.1:5000/questions`<br>

	{
      	 'success': True, // The status of the request, if the result is always the value true.
         'questions'{
                	[
			 "id", // A unique identifier for each question.
			 "question" // The essence of the question.
			 "category" // The category identifier that this question belongs to.
			 "difficulty" // The difficulty level of the question.
			 "answer" // answer question
			],
			.... // Displays all questions.
         'total_questions', // Number all questions on the database.
         'categories': {
                [
		 "id", // Unique identifier for a category.
		 "type", // Name of category.
		 "counter" // question counter for each category.
		],
		.... // Displays all categories.
         'current_category': None,
    	}


#### DELETE /questions/\<int:id\>

* General:
  * Deletes a question by id using url parameters.
  * Returns id of deleted question upon success.
* Sample: `curl http://127.0.0.1:5000/questions/6 -X DELETE`<br>

        {
            "deleted": 6, 
            "success": true
        }



#### POST /questions

This endpoint either creates a new question or returns search results.

1. If <strong>no</strong> search term is included in request:

* General:
  * Creates a new question using JSON request parameters.
  * Returns JSON object with newly created question, as well as paginated questions.
* Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{
            "question": "Which US state contains an area known as the Upper Penninsula?",
            "answer": "Michigan",
            "difficulty": 3,
            "category": "3"
        }'`<br>


        {
            "created": 173, 
            "question_created": "Which US state contains an area known as the Upper Penninsula?", 
            "questions": [
                {
                    "answer": "Apollo 13", 
                    "category": 5, 
                    "difficulty": 4, 
                    "id": 2, 
                    "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
                }, 
		.....//
            ], 
            "success": true, 
            "total_questions": 20
        }



2. If search term <strong>is</strong> included in request:

* General:
  * Searches for questions using search term in JSON request parameters.
  * Returns JSON object with paginated matching questions.
* Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "which"}'`<br>



        {
            "questions": [
                {
                    "answer", 
                    "category", 
                    "difficulty", 
                    "id", 
                    "question""
                }, 
		....// Returns all questions matching the keyword.
            "success": true, 
            "total_questions": 18
        }


#### GET /categories/\<int:id\>/questions

* General:
  * Gets questions by category id using url parameters.
  * Returns JSON object with paginated matching questions.
* Sample: `curl http://127.0.0.1:5000/categories/1/questions`<br>


        {
            "current_category": "Science", 
            "questions": [
                {
                    "answer", 
                    "category", 
                    "difficulty", 
                    "id", 
                    "question"
                }, 
		.../// Returns the number of questions by agreement of the limit of questions in one page.
            ], 
            "success": true, 
            "total_questions": 18
        }
	
	

#### POST /quizzes

* General:
  * Allows users to play the quiz game.
  * Uses JSON request parameters of category and previous questions.
  * Returns JSON object with random question not among previous questions.
* Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [20, 21],
                                            "quiz_category": {"type": "Science", "id": "1"}}'`<br>

        {
            "question": {
                "answer", 
                "category", 
                "difficulty", 
                "id", 
                "question"
            }, 
            "success": true
        }
	
	
## Authors
SaidAbbos. khudoykulov
abbos.xudoyqulov@gmail.com
21.04.2020
This API program is designed for the task of a tutor on the course of udacity fullstack developer.
