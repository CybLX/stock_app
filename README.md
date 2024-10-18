# Stock Sentinel using Selenium and WhatsApp

## Overview
This project is a stock monitoring application that uses **Selenium WebDriver** to fetch stock data and communicates with users via **WhatsApp Web**. The system runs entirely on your machine, providing various functionalities such as real-time stock price checks, database updates, daily monitoring, and keyword-based news searches. However, note that this application requires a stable connection to WhatsApp Web for remote communication.

## Dataset Features
The local database of the application tracks stock data such as the current price, historical trends, and news articles related to the stocks you're monitoring. All updates are stored locally on your machine for privacy and ease of access.

## Project Goals
The primary goal of this project is to provide a convenient, remote way to monitor stock prices and receive updates via WhatsApp. It allows you to:
- **Check** the current value of a stock.
- **Update** the local database with any new information.
- **Monitor** stock prices daily, predicting trends for the next 7 days.
- **Search** for the latest news related to a stock based on keywords.

## Tools Used
- **Selenium WebDriver** for web scraping.
- **WhatsApp Web** for remote communication.
- **Python** for backend logic and interaction with WhatsApp.
- **SQLite** for the local database.

## How to Use

### 1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/cyblx/stock_app.git
   ```

### 2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Open WhatsApp Web and ensure you have a stable connection:
   - The app uses WhatsApp Web to send alerts and updates, so make sure your phone is connected to the internet and linked to WhatsApp Web.

### 4. Use the following functionalities:
- **check**: To check the current value of a stock.
- **update**: To fetch updates and update the local database.
- **monitor**: Initialize daily monitoring to predict stock trends for the next 7 days. Alerts will be sent for any major fluctuations.
- **pesquisa (search)**: Perform a keyword-based news search and return a list of the most recent articles.

## Important Notes for Users:
1. The application communicates via WhatsApp, making it remote, but **a stable WhatsApp Web connection** is required at all times.

2. **Update limitations**:
   - The function `diario(self, ativo, update=1, batch_size=5)` is currently **broken** due to **!>@%$#?$ anti-bot protection** on the !#&@#$%$^%)@ website. This means the database update using update type 1 is not functional at the moment.

3. **Prediction model**:
   - The function `load_predict(ativo)` is a placeholder. It **does not provide a real prediction**. You will need to initialize your own model or replace this function with one that uses a trained model for accurate predictions.

## For More Information
For more information, codes, tutorials, and exciting projects, visit the links below:

- Email: alves_lucasoliveira@usp.br
- GitHub: [CYBLX](https://github.com/cyblx)
- LinkedIn: [CYBLX](https://www.linkedin.com/in/cyblx)
