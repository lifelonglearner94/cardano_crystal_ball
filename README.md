# Cardano Crystal Ball Cryptocurrency Price Prediction

Cardano (ADA) is a blockchain network known for its environmental friendliness compared to Bitcoin. ADA serves as Cardano’s native cryptocurrency and is one of the largest in the crypto market.

## Context

ADA’s high volatility presents both risks and opportunities. Prices are influenced by various factors, making it an exciting space for potential profits.

## Data

Our project leverages the following data sources:

- **Price of ADA:** We’ve collected hourly ADA price data over the past five years.
- **Fear and Greed Index:** Monitoring market sentiment.
- **Google Trends:** Analyzing relevant keywords.

## Tech Stack

Our project utilizes the following technologies:

- Python
- Fast API
- Docker
- Google Cloud
- Darts Time Series Library
- Streamlit

## Models

We’ve implemented the following models for predicting ADA prices:

- **RNN (LSTM):** Excellent for time series data prediction.
  - Input: 5 days of historical data
  - Target: Predicting ADA price for the next 24 hours

## Installation Instructions

To set up the project locally, follow these steps:

1. Clone this repository: `git clone https://github.com/your-username/Cardano-Crystal-Ball.git`
2. Navigate to the project directory: `cd Cardano-Crystal-Ball`
3. Install dependencies: `pip install -r requirements.txt`
4. Go to our streamlit repo: https://github.com/lifelonglearner94/cardano-crystal-ball-website
5. Run the Streamlit app there: `streamlit run app.py`

## Usage

1. Run the Streamlit app using the instructions above.
2. Access the app in your browser (usually at http://localhost:8501).
3. Input relevant parameters (e.g., historical data, prediction horizon) to view ADA price predictions.

## Contributing Guidelines

We welcome contributions! If you’d like to contribute to the project, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with clear descriptions and relevant tests.


## Contact Information

Feel free to reach out to us and open an issue on our GitHub repository.

Happy coding! 🚀
