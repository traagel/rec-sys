# Foxway Data Engineering Homework Assignment

This project involves setting up a MongoDB database in a Docker container and conducting exploratory data analysis (EDA) on a dataset provided by Foxway.

## Project Structure

This project consists of several main directories and files:

- `customers.csv` and `products.csv`: These CSV files contain customer and product data, respectively.

- `data`: This directory contains all relevant data files used in this project, including serialized data files, saved models, and index mappings. 

- `data_exploration.ipynb`, `data_exploration2.ipynb`, `data_exploration3.ipynb`: These Jupyter notebooks were used for exploring the dataset, gaining insights, and performing preliminary analyses.

- `model.ipynb`: A Jupyter notebook used for training the machine learning model and evaluating its performance.

- `db_service`: This directory includes a Dockerfile and scripts necessary to set up and run the MongoDB service, a NoSQL database used for this project.

- `model_training_service`: This is the main service of this project. It includes Python scripts for data preparation, model training, recommendation generation, and a Flask web application (`app.py`). 

- `docker-compose.yml`: A Docker Compose file to define and run multi-container Docker applications. It provides an easy way to manage the different services (like the database and model training service).

- `logs`: A directory that stores log files generated by the application. This can be helpful for debugging and tracking the application's activities over time.


## Getting Started

These instructions will help you get a copy of the project up and running on your local machine.

### Prerequisites

- Docker
- Python 3.8 or later
- PyMongo
- Pandas

### Installation

## Installation

1. Clone the repository to your local machine.

    ```shell
    git clone https://github.com/traagel/rec-sys.git
    ```

2. Navigate to the project directory.

    ```shell
    cd rec-sys
    ```

3. Run the Docker containers using Docker Compose. This command will build and start all services defined in your Docker Compose file.

    ```shell
    docker compose up
    ```

    The model training service will start a Flask server that listens for POST requests on port 5000.

4. Send a POST request to the /recommend endpoint, for example using curl
    
    ```shell
    curl -X POST -H "Content-Type: application/json" -d '{"customername":"caf0fc6bf1f16076cec4a3394c07267d"}' http://172.19.0.3:5000/recommend
    ```
    

## Built With

- Docker
- MongoDB
- Python
- PyMongo
- Pandas

