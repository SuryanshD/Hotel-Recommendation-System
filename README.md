# Hotel Booking Recommendation System

A hotel booking web application that allows users to search, view, and reserve hotel rooms online. And application will recommend hotels using multiple ML algorithms to recommend hotels based on user preferences and past booking history.

## Features

- User registration and authentication
- Search hotels by location, date, and amenities
- View hotel details, photos, and reviews
- Book and manage reservations
- Recomment hotels using ML

## Technologies Used

- Django ="^5.2.1"
- scikit-surprise = "^1.1.4"
- pandas = "^2.2.3"
- scikit-learn = "^1.6.1"

## Getting Started
Run the application in local by folowing the steps:

1. Clone the repository from github
2. Navigate to the project directory
3. Install the required dependencies using pip
```
pip install poetry
```
```
poetry install
````
4. Migrate the model changes to DB
```
python manage.py makemigrations
``` 
```
python manage.py migrate
```
5. Run the application
```
python manage.py runserver
```
6. Access the aapplication in your web browser at http://localhost:8000/

