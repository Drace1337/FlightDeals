# Flight Deals Finder

## Project Description
Flight Deals Finder is an application for searching cheap flights between selected cities. The project utilizes an API for flight search and an Excel file for storing and updating flight data.

## Features
- Retrieving IATA codes for cities.
- Searching for the cheapest flights for specified cities and dates.
- Storing flight data in an Excel file.
- Running the application inside a Docker container.

## Requirements
- Python 3.13
- Docker and Docker Compose
- A `.env` file containing API keys and authentication data:
  ```plaintext
  AMADEUS_API_KEY=your_api_key
  AMADEUS_API_SECRET=your_api_secret
  IATA_ENDPOINT=your_iata_endpoint
  TOKEN_ENDPOINT=your_token_endpoint
  FLIGHT_OFFERS_ENDPOINT=your_flight_offers_endpoint
  CURRENCY_CODE=your_currency_code
  SHEETY_USERNAME=your_sheety_username
  SHEETY_PROJECT_NAME=your_sheety_project_name
  SHEET_NAME=your_sheet_name
  ```

## Installation and Execution
### Running Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/flight-deals.git
   cd flight-deals
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

### Running with Docker
1. Clone the repository and navigate to the project directory:
   ```bash
   git clone https://github.com/yourusername/flight-deals.git
   cd flight-deals
   ```
2. Start the application in a container:
   ```bash
   docker-compose run --rm backend
   ```

## Author
- **Drace** - [Your GitHub](https://github.com/Drace1337)

