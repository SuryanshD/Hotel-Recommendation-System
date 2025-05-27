# Hotel Booking Recommendation System

A hotel booking web application that allows users to search, view, and reserve hotel rooms online. And application will recommend hotels using multiple ML algorithms to recommend hotels based on user preferences and past booking history.

## Run the application with docker

1. Build Image
    1.1 Build the docker from local
    ```
    docker build -t hotel-booking-recommendation-system . 
    ```
    1.2 Build the docker from docker hub
    ```
    docker pull username/hotel-booking-recommendation-system
    ```
2. Run the docker image
```
docker run -d -p 8000:8000 --name hotel-booking hotel-recommendation-system
```
3. Access the aapplication in your web browser at http://localhost:8000/

