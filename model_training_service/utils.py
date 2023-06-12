import logging
import os

import pandas as pd


def setup_logging(file_name):
    # logging folder
    log_folder = '../logs/'
    file_name = file_name + '-' + str(pd.Timestamp.now().date()) \
                + str(pd.Timestamp.now().time()) \
                    .replace(':', '-') + '.log'

    # if folder does not exist, create it
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    logging.basicConfig(filename=log_folder + file_name, level=logging.INFO)

    # console handler
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    logging.getLogger().addHandler(c_handler)
