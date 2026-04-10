import os
import pandas as pd
#import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error
from math import sqrt

from model import build_lstm_model
from preprocessing import create_sequences, scale_data

DATA_PATH = "C:/Crime rate prediction by region using LSTM/Crime rate Prediction Project/data/crime_data_india.csv"
TIME_STEP = 5
EPOCHS = 50

def train_all_states():

    df = pd.read_csv(DATA_PATH)
    df = df[['STATE/UT', 'YEAR', 'TOTAL IPC CRIMES']]
    df = df.dropna()

    states = df['STATE/UT'].unique()

    os.makedirs("../saved_models", exist_ok=True)
    os.makedirs("../saved_scalers", exist_ok=True)
    os.makedirs("../outputs/plots", exist_ok=True)

    for state in states:
        print(f"\nTraining model for: {state}")

        state_df = df[df['STATE/UT'] == state].sort_values("YEAR")
        values = state_df['TOTAL IPC CRIMES'].values

        if len(values) <= TIME_STEP:
            print(f"Skipping {state} (not enough data)")
            continue

        scaled, scaler = scale_data(values)
        X, y = create_sequences(scaled, TIME_STEP)

        split = int(len(X) * 0.8)
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]

        X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
        X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

        model = build_lstm_model(TIME_STEP)
        model.fit(X_train, y_train, epochs=EPOCHS, batch_size=8, verbose=1)

        y_pred = model.predict(X_test)

        y_test_inv = scaler.inverse_transform(y_test)
        y_pred_inv = scaler.inverse_transform(y_pred)

        rmse = sqrt(mean_squared_error(y_test_inv, y_pred_inv))
        mae = mean_absolute_error(y_test_inv, y_pred_inv)

        print(f"{state} RMSE: {rmse:.2f}")
        print(f"{state} MAE: {mae:.2f}")

        plt.figure()
        plt.plot(y_test_inv, label="Actual")
        plt.plot(y_pred_inv, label="Predicted")
        plt.title(f"{state} Prediction")
        plt.legend()
        plt.savefig(f"../outputs/plots/{state}.png")
        plt.close()

        model.save(f"../saved_models/{state}_lstm.h5")
        joblib.dump(scaler, f"../saved_scalers/{state}_scaler.pkl")

    print("\nAll states trained successfully!")

if __name__ == "__main__":
    train_all_states()