# Flight Search Application

A full-stack web application for searching flights, managing user accounts, and tracking search history. Built with React frontend and Flask backend, using the Amadeus API for flight data.

## Features

- **User Authentication**: Register, login, and profile management
- **Flight Search**: Search for flights by city with detailed criteria
- **IATA Code Resolution**: Automatically resolve city names to airport codes
- **Search History**: Save and view previous flight searches
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Flight Data**: Integration with Amadeus API for live flight information

## Tech Stack

### Frontend
- **React 18** with Vite
- **React Router** for navigation
- **SCSS** for styling
- **Axios** for API calls
- **Font Awesome** for icons

### Backend
- **Flask** with Python 3.13
- **SQLAlchemy** for database ORM
- **PostgreSQL** for data storage
- **JWT** for authentication
- **Flask-CORS** for cross-origin requests
- **Amadeus API** for flight data

### Infrastructure
- **Docker & Docker Compose** for containerization
- **PostgreSQL** database
- **pgAdmin** for database management
- **Nginx** for frontend serving

## Prerequisites

- Docker and Docker Compose
- Amadeus API credentials (API Key and Secret)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd flight-search-app
```

### 2. Environment Configuration

Create the following environment files:

#### `env/postgres.env`
```env
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_DB=flight_deals_db
SQLALCHEMY_DATABASE_URI=postgresql://your_db_user:your_db_password@postgres:5432/flight_deals_db
```

#### `env/backend.env`
```env
SECRET_KEY=your_secret_key_here
AMADEUS_API_KEY=your_amadeus_api_key
AMADEUS_API_SECRET=your_amadeus_api_secret
TOKEN_ENDPOINT=https://test.api.amadeus.com/v1/security/oauth2/token
IATA_ENDPOINT=https://test.api.amadeus.com/v1/reference-data/locations
FLIGHT_OFFERS_ENDPOINT=https://test.api.amadeus.com/v2/shopping/flight-offers
CURRENCY_CODE=EUR
```

#### `env/pgadmin.env`
```env
PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=admin
```

### 3. Amadeus API Setup

1. Go to [Amadeus Developers](https://developers.amadeus.com/)
2. Create a free account
3. Create a new app to get your API Key and Secret
4. Add the credentials to `env/backend.env`

### 4. Start the Application

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **pgAdmin**: http://localhost:5050

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

### Flight Search
- `GET /search/iata?city={city}` - Get IATA codes for a city
- `GET /search/flights` - Search flights with parameters
- `POST /search/save` - Save search to history

### User Profile
- `GET /profile` - Get user profile
- `PUT /profile` - Update user profile
- `PUT /profile/password` - Update password

### Search History
- `GET /history` - Get user's search history

## Usage Guide

### 1. User Registration/Login
- Navigate to the login page
- Register a new account or login with existing credentials
- Authentication is required for flight searches

### 2. Searching Flights
1. Enter departure and destination cities
2. Select specific airports from the dropdown
3. Choose departure and return dates
4. Specify number of passengers
5. Search for available flights
6. View detailed flight information including:
   - Airlines and flight numbers
   - Departure/arrival times
   - Flight duration
   - Prices and cabin class
   - Number of stops

### 3. Managing Profile
- Update personal information (name, email)
- Change password
- View account details

### 4. Search History
- View all previous flight searches
- See search dates and routes
- Access saved search criteria

## Development

### Local Development Setup

#### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
flask run
```

#### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Project Structure

```
flight-search-app/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models
│   │   ├── routes/          # API routes
│   │   ├── services/        # Business logic
│   │   └── __init__.py      # Flask app factory
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   └── styles/          # SCSS styles
│   ├── Dockerfile
│   └── package.json
├── env/                     # Environment files
└── docker-compose.yml
```

### Adding New Features

1. **Backend**: Add new routes in `backend/app/routes/`
2. **Frontend**: Create components in `frontend/src/components/`
3. **Database**: Add models in `backend/app/models/`
4. **Styles**: Add SCSS files in `frontend/src/styles/`

## Database Schema

### Users Table
- `id` (Primary Key)
- `name` (String, Required)
- `email` (String, Unique, Required)
- `password` (String, Hashed, Required)
- `created_at` (DateTime)

### Search History Table
- `id` (Primary Key)
- `user_id` (Foreign Key to Users)
- `origin` (String, IATA Code)
- `destination` (String, IATA Code)
- `departure_date` (Date)
- `return_date` (Date)
- `created_at` (DateTime)

## Troubleshooting

### Common Issues

1. **Amadeus API Errors**
   - Check API credentials in environment file
   - Verify API endpoint URLs
   - Ensure API rate limits aren't exceeded

2. **Database Connection Issues**
   - Verify PostgreSQL is running
   - Check database credentials
   - Ensure database exists

3. **CORS Issues**
   - Frontend and backend origins are configured
   - Check CORS settings in Flask app

4. **Authentication Problems**
   - Verify JWT token is being sent
   - Check token expiration
   - Ensure user is properly registered

### Logs

View application logs:
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Create an issue in the repository
