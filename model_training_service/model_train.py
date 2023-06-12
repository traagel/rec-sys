# load the train and test sets
import logging
import os
import pickle

from sklearn.linear_model import LinearRegression

from utils import setup_logging


def main():
    setup_logging('model-train')

    logging.info('Starting model training, logging to ../logs/model-train-<date>.log')
    try:
        with open('../data/customer/model_data.pkl', 'rb') as f:
            data_loaded = pickle.load(f)

        logging.info('Data loaded')
    except FileNotFoundError:
        logging.error('File not found')
        exit(1)

    X_train = data_loaded['X_train']
    y_train = data_loaded['y_train']

    # Create and train the model
    logging.info('Creating and training the model')
    model = LinearRegression()
    model.fit(X_train, y_train)

    logging.info('Model created and trained')
    # Save the model
    filename = '../data/customer/model.sav'
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    pickle.dump(model, open(filename, 'wb'))
    logging.info('Model saved to ' + filename)


if __name__ == '__main__':
    main()
