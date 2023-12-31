# -*- coding: utf-8 -*-
"""bharth intern task _1

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OjU5LPnSkAg4FD8p_wirMtJUMBMR5Dmw
"""

# Import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.metrics import mean_squared_error

# Download historical stock price data
ticker_symbol = "AAPL"  # Example: Apple Inc. stock
start_date = "2010-01-01"
end_date = "2021-01-01"
data = yf.download(ticker_symbol, start=start_date, end=end_date)

# Extract the closing price
df = data[['Close']]

# Normalize the data
scaler = MinMaxScaler()
df['Close'] = scaler.fit_transform(df['Close'].values.reshape(-1, 1))

# Split the data into training and testing sets
train_size = int(len(df) * 0.8)
train_data, test_data = df[:train_size], df[train_size:]

# Create sequences for the LSTM model
def create_sequences(data, seq_length):
    sequences = []
    target = []
    for i in range(len(data) - seq_length):
        seq = data[i:i+seq_length]
        label = data[i+seq_length]
        sequences.append(seq)
        target.append(label)
    return np.array(sequences), np.array(target)

seq_length = 10  # Number of previous days' closing prices to use for prediction
X_train, y_train = create_sequences(train_data.values, seq_length)
X_test, y_test = create_sequences(test_data.values, seq_length)

# Build the LSTM model
model = Sequential()
model.add(LSTM(50, activation='relu', input_shape=(seq_length, 1)))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=32)

# Make predictions on the test data
predicted_stock_prices = model.predict(X_test)

# Inverse transform the predictions to get actual prices
predicted_stock_prices = scaler.inverse_transform(predicted_stock_prices)

# Calculate Mean Squared Error
mse = mean_squared_error(test_data[seq_length:], predicted_stock_prices)
print("Mean Squared Error:", mse)

# Visualize the results
plt.figure(figsize=(12, 6))
plt.plot(test_data.index[seq_length:], test_data[seq_length:], label='Actual Price')
plt.plot(test_data.index[seq_length:], predicted_stock_prices, label='Predicted Price')
plt.legend()
plt.title(f'{ticker_symbol} Stock Price Prediction')
plt.show()