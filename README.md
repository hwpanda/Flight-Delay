# Flight Delay Prediction App

This application predicts flight delays using a machine learning model (XGBoost). It provides a web interface for users to input flight details and visualizes the route on a map.

## Prerequisites

- Python 3.10 or higher
- `pip` (Python package installer)
- `libomp` (Required for XGBoost on macOS)

## Installation

1.  **Navigate to the project directory**.

2.  **Set up a virtual environment** (recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies**:
    ```bash
    pip install flask xgboost pandas scikit-learn
    ```

    > **Note for macOS users:** If you encounter an error loading XGBoost (e.g., `Library not loaded: @rpath/libomp.dylib`), you need to install `libomp` using Homebrew:
    > ```bash
    > brew install libomp
    > ```

## Usage

1.  **Run the application**:
    Make sure you are using the python executable from your virtual environment:
    ```bash
    ./venv/bin/python app.py
    ```
    (Or just `python app.py` if you have already activated your virtual environment).

2.  **Open your browser** and navigate to:
    [http://127.0.0.1:5000](http://127.0.0.1:5000)

3.  **Predict a Delay**:
    - Select a **Flight Date**.
    - Enter **Scheduled Departure** and **Arrival** times.
    - Select an **Airline** from the dropdown.
    - Enter **Origin** and **Destination** airport codes (e.g., ATL, JFK).
    - Click **Predict**.

4.  **View Results**:
    - A banner will display the prediction (Delayed/On Time) and the probability.
    - A map will show the flight route.
    - A table will list the features used for the prediction.

## Project Structure

- `app.py`: Main Flask application entry point and route definitions.
- `services/`: Modular backend services.
    - `model_service.py`: Handles model loading and prediction.
    - `weather_service.py`: Handles weather data loading and lookup.
    - `woe_service.py`: Handles WOE (Weight of Evidence) map loading.
    - `data_service.py`: Handles static data loading (airports, airlines).
- `templates/index.html`: Frontend HTML template.
- `static/js/app.js`: Frontend JavaScript logic.
- `model/`: Contains the trained XGBoost model.
- `data/`: Contains airport, airline, and weather data.
