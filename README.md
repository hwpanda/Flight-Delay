# Flight Delay Prediction App

This application predicts flight delays using a machine learning model (XGBoost). It provides a web interface for users to input flight details and visualizes the route on a map.

## Prerequisites

- Python 3.10 or higher
- `pip` (Python package installer)
- Node.js 20 or higher and `npm` (for the React frontend)
- `libomp` (Required for XGBoost on macOS)

## Installation

1.  **Navigate to the project directory**.

2.  **Set up a virtual environment** (recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install Python dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

    > **Note for macOS users:** If you encounter an error loading XGBoost (e.g., `Library not loaded: @rpath/libomp.dylib`), you need to install `libomp` using Homebrew:
    > ```bash
    > brew install libomp
    > ```

## Usage

1.  **Build the React frontend**:
    ```bash
    cd frontend
    npm install
    npm run build
    cd ..
    ```

2.  **Run the application**:
    Make sure you are using the python executable from your virtual environment:
    ```bash
    ./venv/bin/python app.py
    ```
    (Or just `python app.py` if you have already activated your virtual environment).

3.  **Open your browser** and navigate to:
    [http://127.0.0.1:5000](http://127.0.0.1:5000)

4.  **Predict a Delay**:
    - Select a **Flight Date**.
    - Enter **Scheduled Departure** and **Arrival** times.
    - Select an **Airline** from the dropdown.
    - Enter supported **Origin** and **Destination** airport codes (e.g., ATL, BOS).
    - Click **Predict delay**.

5.  **View Results**:
    - A prediction card will display the likely outcome and probability.
    - A map will show the flight route.

For frontend-only development, run Flask as above and use `npm run dev` from
`frontend/`. Vite proxies API calls to Flask at port 5000.

## Project Structure

- `app.py`: Main Flask application entry point and route definitions.
- `services/`: Modular backend services.
    - `model_service.py`: Handles model loading and prediction.
    - `weather_service.py`: Handles weather data loading and lookup.
    - `woe_service.py`: Handles WOE (Weight of Evidence) map loading.
    - `data_service.py`: Handles static data loading (airports, airlines).
- `templates/index.html`: Minimal Flask shell that loads the compiled frontend.
- `frontend/`: Vite, React, and TypeScript source for the user interface.
- `static/react/`: Generated React assets; create them with `npm run build`.
- `model/`: Contains the trained XGBoost model.
- `data/`: Contains airport, airline, and weather data.
