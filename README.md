# Titanic Survival Prediction API

<img src="https://upload.wikimedia.org/wikipedia/commons/6/6e/St%C3%B6wer_Titanic.jpg" alt="titanic" width="500" height="400">


This is a RESTful API that provides survival predictions for passengers on the Titanic based on their attributes such as passenger class, gender, embarked port, family size, fare, and age. The API is built using Flask and serves the `swagger.json` file for API documentation.

## API Documentation

You can find the detailed API documentation in the [swagger.json](https://github.com/ErikaMelt/data-ship-api/tree/main/api/static/swagger.json) file. This file follows the OpenAPI 3.0.3 specification and contains all the necessary information about the API endpoints, request parameters, and response schemas.

<img src="https://github.com/ErikaMelt/data-ship-api/blob/main/images/swagger_docs.png" alt="Swagger UI" width="500" height="300">


## Architecture

The Titanic Survival Prediction API is built using the following components:

- Flask: A lightweight and flexible web framework for Python.
- Flask-Restful: An extension for Flask that adds support for quickly building REST APIs.
- Flask-Swagger-UI: An extension for Flask that integrates Swagger UI to visualize and interact with the API documentation.

The API follows a simple client-server architecture, where the client sends a POST request with passenger information, and the server responds with the survival prediction and probabilities.

## Installation

To run the API locally, follow these steps:

1. Clone the repository:
git clone https://github.com/ErikaMelt/data-ship-api.git
2. Install the required dependencies using `pip`:
pip install -r requirements.txt


3. Run the API server:
python app.py


4. Access the API documentation:

Swagger UI: [http://localhost:5000/api/docs/](http://localhost:5000/api/docs/)

## API Endpoints

### POST /predict

This endpoint is used to make survival predictions for passengers on the Titanic based on their attributes.

#### Request Body

The request body should be a JSON object with the following attributes:

- `passenger_class` (str): Passenger class, should be 'first', 'second', or 'third'.
- `gender` (str): Gender of the passenger, should be 'male' or 'female'.
- `embarked_from` (str): Port of embarkation, should be 'Southampton', 'Queenstown', or 'Cherbourg'.
- `family_size` (int): Number of family members.
- `fare` (float): Fare amount.
- `age` (int): Age of the passenger.

#### Response

The API responds with a JSON object containing the following attributes:

- `predictions` (list of int): List of prediction results (0 or 1) for each input. The output prediction can be interpreted as 1 Survival and 0 Non survival. 
- `probabilities` (list of float): List of prediction probabilities for each class Survival and Non Survival. 

Example:

POST /predict
{
"passenger_class": "first",
"gender": "female",
"embarked_from": "Cherbourg",
"family_size": 2,
"fare": 100.0,
"age": 35
}

Response:
{
"predictions": [1],
"probabilities": [[0.2, 0.8]]
}

<img src="https://github.com/ErikaMelt/data-ship-api/blob/main/images/postman_post.png" alt="Swagger UI" width="500" height="300">


### GET /ping

This endpoint is used to check the health status of the API.

#### Response

The API responds with a JSON object containing the message "API is alive".

Example:

GET /ping

Response:
{
"message": "API is alive"
}


## License

This project is licensed under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0.html). Feel free to use and modify the code according to the terms of the license.

## Author

Created by [Erika](https://github.com/ErikaMelt)
For any questions or inquiries, please contact me at: erikapaolaortiz@gmail.com

