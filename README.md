# Foxway Data Engineering Homework Assignment

This project involves setting up a MongoDB database in a Docker container and conducting exploratory data analysis (EDA) on a dataset provided by Foxway.

## Project Structure

Here's the layout of the project:

- `Dockerfile`: The Dockerfile for building the Docker image, which runs a MongoDB instance and imports the dataset into a database.
- `mongo_script.sh`: A bash script that initializes the MongoDB database and collection and imports the data from a JSON file.
- `data_exploration.py`: A Python script for performing EDA on the data stored in MongoDB.
- `data/dataset_engineer.json`: The provided dataset, which is ignored by Git. You should replace it with your own data file.

## Getting Started

These instructions will help you get a copy of the project up and running on your local machine.

### Prerequisites

- Docker
- Python 3.8 or later
- PyMongo
- Pandas

### Installation

1. Clone the repository to your local machine.
2. Build the Docker image using the provided Dockerfile and run the container.
3. Use `data_exploration.py` to connect to the database and perform EDA.

## Built With

- Docker
- MongoDB
- Python
- PyMongo
- Pandas

## Authors

- Mart Traagel - v0.1

## Acknowledgments

- Foxway for providing the dataset and the assignment.
