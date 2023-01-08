def main():
    '''
    This script will be executed every business hour
    '''
    # 1. Retrieve models to be computed
    models = retrieve_models()

    # 2. Pull tickers
    # 2a. Retrieve from model list the list of tickers to be pulled
    # 2b. Pull tickers and save them to database
    tickers = pull_tickers()

    # 3. Compute features
    # 3a. Build a linked list of features
    # 3b. Compute each of them and save to database
    features = compute_features(tickers)

    # 4. Execute models
    for model in models:
        model.execute()

    # 5. Build portfolio

    # 6. Call broker

    # 7. Compute Post Thread Stats