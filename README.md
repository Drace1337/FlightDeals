# Flight Deals Finder

## Opis projektu
Flight Deals Finder to aplikacja do wyszukiwania tanich lotów pomiędzy wybranymi miastami. Projekt wykorzystuje API do wyszukiwania lotów oraz plik Excel do przechowywania i aktualizacji danych o lotach.

## Funkcjonalności
- Pobieranie kodów IATA dla miast.
- Wyszukiwanie najtańszych lotów dla podanych miast i dat.
- Przechowywanie danych o lotach w pliku Excel.
- Możliwość uruchomienia aplikacji w kontenerze Docker.

## Wymagania
- Python 3.13
- Docker i Docker Compose
- Plik `.env` z kluczami API i danymi uwierzytelniającymi:
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

## Instalacja i uruchomienie
### Uruchomienie lokalne
1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/yourusername/flight-deals.git
   cd flight-deals
   ```
2. Zainstaluj wymagane pakiety:
   ```bash
   pip install -r requirements.txt
   ```
3. Uruchom aplikację:
   ```bash
   python main.py
   ```

### Uruchomienie z Docker
1. Sklonuj repozytorium i przejdź do katalogu projektu:
   ```bash
   git clone https://github.com/yourusername/flight-deals.git
   cd flight-deals
   ```
2. Uruchom aplikację w kontenerze:
   ```bash
   docker-compose up --build
   ```

## Struktura projektu
```
flight-deals/
│── backend/
│   │── main.py
│   │── data_manager.py
│   │── flight_search.py
│   │── flight_data.py
│   │── requirements.txt
│   │── Flight_Deals.xlsx
│   │── .env
│── Dockerfile
│── docker-compose.yml
│── README.md
```

## Autor
- **Drace** - [Twój GitHub](https://github.com/Drace1337)

