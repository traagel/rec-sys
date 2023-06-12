import argparse
import logging
import pickle

import numpy as np

from utils import setup_logging


def recommend_products(model, user_id, product_features_combined, U, N=5):
    # Get the user's features from the 'U' matrix
    user_features = U[user_id]

    # Create feature vectors for each item
    feature_vectors = [np.concatenate([user_features, product_features]) for product_features in
                       product_features_combined]

    # Predict the interaction values
    predicted_interactions = model.predict(feature_vectors)

    # Rank the items based on the predicted interactions
    ranked_items = np.argsort(predicted_interactions)[::-1]

    # Select the top-N items
    recommended_items = ranked_items[:N]

    return recommended_items


def reverse_mapping(products, product_index_mapping):
    # return key for value - i know it's bad but it's 3am
    return [key for key, value in product_index_mapping.items() if value in products]


def predict(username, N=5):
    setup_logging('recommend')

    logging.info('Starting recommendation, logging to ../logs/recommend-<date>.log')
    try:
        with open('../data/customer/model_data.pkl', 'rb') as f:
            data_loaded = pickle.load(f)
    except FileNotFoundError:
        logging.error('File not found')
        exit(1)

    U = data_loaded['U']
    product_features_combined = data_loaded['product_features_combined']
    customer_index_mapping = data_loaded['customer_index_mapping']
    product_index_mapping = data_loaded['product_index_mapping']

    # top5_sold_products_list = data_loaded['top5_sold_products_list']

    model_path = '../data/customer/model.sav'
    model = pickle.load(open(model_path, 'rb'))

    user_index = customer_index_mapping[username]

    logging.info('Model loaded')
    logging.info('Predicting for ' + username + ', index: ' + str(user_index))
    try:
        products = recommend_products(model, user_index, product_features_combined.values, U, N)
        products = reverse_mapping(products, product_index_mapping)

    except Exception as e:
        logging.error('Error: ' + str(e))
        # products = top5_sold_products_list
        exit(1)

    logging.info('Products recommended for ' + username + ': ' + str(products))

    return products


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Predict products for a customer")
    parser.add_argument('--customer', type=str, help="Customer ID")

    args = parser.parse_args()
    try:
        customer = args.customer
        result = predict(customer)
        print(result)
    except IndexError:
        logging.error('Not enough products')
        exit(1)
    except Exception as e:
        logging.error('Unknown error: ' + str(e))
        exit(1)
