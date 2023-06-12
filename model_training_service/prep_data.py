import logging
import os
import pickle
import sys
import time

import numpy as np
import pandas as pd
import psutil
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import svds
from sklearn.model_selection import train_test_split
from tqdm import tqdm

from utils import setup_logging


class ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.
    """

    def filter(self, record):
        record.memory = psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2  # memory usage in MB
        record.time = time.asctime()  # current time
        return True


def main():
    setup_logging('prep-data')

    logging.info('Starting data preparation, logging to ../logs/prep-data-<date>.log')
    try:
        logging.info('Connecting to MongoDB database')
        # Create a client connection to your MongoDB instance
        client = MongoClient('mongodb://root:password@db_service:27017')

        # Connect to your database
        db = client['proc-rec-db']

        # Connect to your collection
        collection = db['dataset_engineer']

        # Convert entire collection to Pandas dataframe
        data = pd.DataFrame(list(collection.find()))
        logging.info('Data loaded from MongoDB database')
    except ConnectionFailure:
        logging.info("Could not connect to MongoDB database")
        sys.exit(1)
    except Exception as e:
        logging.info("Unexpected error:" + str(e))
        sys.exit(1)

    logging.info('Data preparation started')

    # drop _id column
    data.drop('_id', axis=1, inplace=True)
    # one hot encoding / pandas dummies on itemgroupname, appearanceext, boxedext
    data = pd.get_dummies(data, columns=['itemgroupname', 'appearanceext', 'boxedext'])

    # remove values above 99.5% quantile
    data = data[data['selling_price'] < data['selling_price'].quantile(0.995)]

    # remove values below 0.5% quantile
    data = data[data['selling_price'] > data['selling_price'].quantile(0.005)]

    # remove values 0 and below
    data = data[data['selling_price'] > 0]

    data['purchase_count'] = data.groupby(['customername', 'productname'])['selling_price'].transform('count')

    logging.info('Data preparation finished')

    interaction_matrix = data.pivot_table(index='customername', columns='productname', values='purchase_count',
                                          fill_value=0)

    logging.info('Interaction matrix created')

    interaction_matrix_sparse = csr_matrix(interaction_matrix.values)

    interaction_matrix_float = interaction_matrix_sparse.astype('float')

    # The number of latent factors you want to keep.
    n_latent_factors = 50

    # the `svds` function returns U, sigma and Vt.
    U, sigma, Vt = svds(interaction_matrix_float, k=n_latent_factors)

    product_features_svd = pd.DataFrame(data=Vt.T, index=interaction_matrix.columns,
                                        columns=[f"latent_{i}" for i in range(n_latent_factors)])
    logging.info('SVD matrix created with ' + str(n_latent_factors) + ' latent factors')

    one_hot_cols = data.columns[
                   data.columns.get_loc('appearanceext_AS-IS'):data.columns.get_loc('boxedext_Unboxed') + 1]

    product_features_one_hot = data.groupby('productname')[one_hot_cols].sum()

    product_features_one_hot = (product_features_one_hot > 0).astype(int)

    product_features_svd.sort_index(inplace=True)
    product_features_one_hot.sort_index(inplace=True)

    product_features_combined = pd.concat([product_features_svd, product_features_one_hot], axis=1)

    logging.info('Product features combined')

    feature_vectors = []
    targets = []

    # Create a dictionary to map customername and productname to their corresponding indices in the interaction matrix
    customer_index_mapping = {customer: i for i, customer in enumerate(interaction_matrix.index)}
    product_index_mapping = {product: i for i, product in enumerate(interaction_matrix.columns)}

    # Iterate over each row in the data
    logging.info('Creating feature vectors and targets')

    for index, row in tqdm(data.iterrows()):
        # Get the user features
        user_id = customer_index_mapping[row['customername']]
        user_features = U[user_id, :]  # Select the corresponding row from the U matrix

        # Get the item features
        product_name = row['productname']
        product_features = product_features_combined.loc[
            product_name].values  # Select the corresponding row from the item features matrix

        # Combine the user and item features into a single feature vector
        feature_vector = np.concatenate([user_features, product_features])

        # Get the target variable (purchase count)
        target = row['purchase_count']

        # Append the feature vector and target to their respective lists
        feature_vectors.append(feature_vector)
        targets.append(target)

    logging.info('Feature vectors and targets created')
    # Convert lists to numpy arrays
    feature_vectors = np.array(feature_vectors)
    targets = np.array(targets)

    logging.info('Splitting data into train and test sets')
    # Split into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(feature_vectors, targets, test_size=0.2, random_state=42)
    # pickle the train and test sets

    directory = '../data/customer/'

    if not os.path.exists(directory):
        logging.info('Creating directory ' + directory)
        os.makedirs(directory)

    top5_sold_products = data.groupby('productname')['purchase_count'].sum().sort_values(ascending=False).head(5).index

    top5_sold_products_list = list(top5_sold_products)

    data_to_save = {
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'data': data,
        'product_features_combined': product_features_combined,
        'customer_index_mapping': customer_index_mapping,
        'product_index_mapping': product_index_mapping,
        'U': U,
        'top5_sold_products': top5_sold_products_list
    }

    with open(directory + 'model_data.pkl', 'wb') as f:
        pickle.dump(data_to_save, f)

    logging.info('Data saved to ' + directory + 'model_data.pkl')


if __name__ == '__main__':
    main()
