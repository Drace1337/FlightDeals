import React, { useState } from 'react';
import FlightSearchForm from '../FlightSearchForm/FlightSearchForm';
import FlightDetailsForm from '../FlightDetailsForm/FlightDetailsForm';
import FlightResults from '../FlightResults/FlightResults';
import SaveSearchModal from '../SaveSearchModal/SaveSearchModal';
import api from '../../../services/api';
import './FlightSearchPage.scss';

// Funkcja do konwersji czasu z formatu PT1H20M na czytelny format
const convertDuration = (ptDuration) => {
    if (!ptDuration) return 'N/A';
    
    const regex = /PT(?:(\d+)H)?(?:(\d+)M)?/;
    const match = ptDuration.match(regex);
    
    if (!match) return ptDuration;
    
    const hours = match[1] ? parseInt(match[1]) : 0;
    const minutes = match[2] ? parseInt(match[2]) : 0;
    
    if (hours > 0 && minutes > 0) {
        return `${hours}h ${minutes}m`;
    } else if (hours > 0) {
        return `${hours}h`;
    } else if (minutes > 0) {
        return `${minutes}m`;
    }
    return 'N/A';
};

// Funkcja do pobierania nazwy linii lotniczej na podstawie kodu IATA
const getAirlineName = (code) => {
    const airlines = {
        'LO': 'LOT Polish Airlines',
        'LH': 'Lufthansa',
        'BA': 'British Airways',
        'AF': 'Air France',
        'KL': 'KLM',
        'SN': 'Brussels Airlines',
        'OS': 'Austrian Airlines',
        'SK': 'SAS',
        'AY': 'Finnair',
        'DL': 'Delta Air Lines',
        'UA': 'United Airlines',
        'AA': 'American Airlines'
    };
    return airlines[code] || code;
};

// Funkcja do transformacji danych z API Amadeus do formatu oczekiwanego przez FlightResults
const transformFlightData = (amadeusData) => {
    if (!Array.isArray(amadeusData)) {
        console.error('Expected array but got:', amadeusData);
        return [];
    }

    return amadeusData.map((flight, index) => {
        try {
            // Pobierz pierwszy segment (lot tam)
            const outboundSegment = flight.itineraries?.[0]?.segments?.[0];
            const returnSegment = flight.itineraries?.[1]?.segments?.[0];
            
            if (!outboundSegment) {
                console.warn('No outbound segment found for flight:', flight);
                return null;
            }

            // Pobierz informacje o cenie
            const price = flight.price?.grandTotal || flight.price?.total || 'N/A';
            const currency = flight.price?.currency || '';
            
            // Pobierz kod linii lotniczej
            const airlineCode = outboundSegment.carrierCode;
            const airlineName = getAirlineName(airlineCode);
            
            // Pobierz informacje o trasie
            const origin = outboundSegment.departure?.iataCode || 'N/A';
            const destination = outboundSegment.arrival?.iataCode || 'N/A';
            
            // Pobierz czas trwania
            const duration = convertDuration(outboundSegment.duration);
            
            // Pobierz klasę
            const fareClass = flight.travelerPricings?.[0]?.fareDetailsBySegment?.[0]?.cabin || 'ECONOMY';
            
            // Pobierz informacje o czasie
            const departureTime = outboundSegment.departure?.at ? 
                new Date(outboundSegment.departure.at).toLocaleTimeString('en-US', { 
                    hour: '2-digit', 
                    minute: '2-digit' 
                }) : 'N/A';
                
            const arrivalTime = outboundSegment.arrival?.at ? 
                new Date(outboundSegment.arrival.at).toLocaleTimeString('en-US', { 
                    hour: '2-digit', 
                    minute: '2-digit' 
                }) : 'N/A';

            return {
                id: flight.id || `flight-${index}`,
                airline: airlineName,
                price: `${price} ${currency}`,
                origin: origin,
                destination: destination,
                duration: duration,
                class: fareClass,
                departureTime: departureTime,
                arrivalTime: arrivalTime,
                stops: outboundSegment.numberOfStops || 0,
                aircraft: outboundSegment.aircraft?.code || 'N/A',
                flightNumber: `${airlineCode} ${outboundSegment.number}`,
                hasReturn: !!returnSegment,
                returnInfo: returnSegment ? {
                    departureTime: returnSegment.departure?.at ? 
                        new Date(returnSegment.departure.at).toLocaleTimeString('en-US', { 
                            hour: '2-digit', 
                            minute: '2-digit' 
                        }) : 'N/A',
                    arrivalTime: returnSegment.arrival?.at ? 
                        new Date(returnSegment.arrival.at).toLocaleTimeString('en-US', { 
                            hour: '2-digit', 
                            minute: '2-digit' 
                        }) : 'N/A',
                    duration: convertDuration(returnSegment.duration),
                    flightNumber: `${returnSegment.carrierCode} ${returnSegment.number}`
                } : null
            };
        } catch (error) {
            console.error('Error transforming flight data:', error, flight);
            return null;
        }
    }).filter(flight => flight !== null); // Usuń nieprawidłowe loty
};

const FlightSearchPage = () => {
    const [step, setStep] = useState(1);
    const [searchData, setSearchData] = useState(null);
    const [flights, setFlights] = useState([]);
    const [showSaveModal, setShowSaveModal] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleCitiesSubmit = async ({ origin, destination }) => {
        setLoading(true);
        setError(null);
        
        try {
            const [originAirports, destinationAirports] = await Promise.all([
                api.get(`/search/iata?city=${origin}`),
                api.get(`/search/iata?city=${destination}`)
            ]);

            setSearchData({
                origin,
                destination,
                originAirports: originAirports.data,
                destinationAirports: destinationAirports.data
            });
            setStep(2);
        } catch (error) {
            console.error('Error fetching airports:', error);
            setError('Failed to fetch airports. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleSearchSubmit = async (details) => {
        setLoading(true);
        setError(null);
        
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                throw new Error('Please login first');
            }

            console.log('Searching flights with params:', {
                origin_iata: details.originIata,
                destination_iata: details.destinationIata,
                departure_date: details.departureDate,
                return_date: details.returnDate || undefined,
                adults: details.adults
            });

            const response = await api.get('/search/flights', {
                params: {
                    origin_iata: details.originIata,
                    destination_iata: details.destinationIata,
                    departure_date: details.departureDate,
                    return_date: details.returnDate || undefined,
                    adults: details.adults
                },
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            console.log('Raw API Response:', response.data);

            // Przekształć dane z API do formatu oczekiwanego przez komponent
            const transformedFlights = transformFlightData(response.data);
            console.log('Transformed flights:', transformedFlights);

            setFlights(transformedFlights);

            // Zapisz szczegóły wyszukiwania
            setSearchData(prevData => ({
                ...prevData,
                originIata: details.originIata,
                destinationIata: details.destinationIata,
                departureDate: details.departureDate,
                returnDate: details.returnDate,
                adults: details.adults
            }));

            setStep(3);
        } catch (error) {
            console.error('Search error:', error);
            setError(`Error: ${error.message}. Please try again.`);
        } finally {
            setLoading(false);
        }
    };

    const handleBackToSearch = () => {
        setStep(1);
        setFlights([]);
        setError(null);
    };

    if (loading) {
        return (
            <div className="flight-search-page">
                <div className="loading-container">
                    <div className="spinner"></div>
                    <p>Searching for flights...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="flight-search-page">
            {error && (
                <div className="error-message">
                    {error}
                    <button onClick={() => setError(null)} className="close-error">×</button>
                </div>
            )}

            {step === 1 && (
                <FlightSearchForm 
                    onSubmit={handleCitiesSubmit}
                    disabled={loading}
                />
            )}
            
            {step === 2 && searchData && (
                <FlightDetailsForm
                    originAirports={searchData.originAirports}
                    destinationAirports={searchData.destinationAirports}
                    onSubmit={handleSearchSubmit}
                    onBack={() => setStep(1)}
                    disabled={loading}
                />
            )}
            
            {step === 3 && (
                <>
                    <div className="results-header">
                        <h2>Search Results</h2>
                        <button 
                            onClick={handleBackToSearch}
                            className="new-search-button"
                        >
                            New Search
                        </button>
                    </div>
                    
                    <FlightResults
                        flights={flights}
                        origin={searchData?.origin}
                        destination={searchData?.destination}
                    />
                    
                    {flights.length === 0 && !loading && (
                        <div className="no-results">
                            <p>No flights found for your search criteria.</p>
                            <button 
                                onClick={handleBackToSearch}
                                className="try-again-button"
                            >
                                Try Different Dates
                            </button>
                        </div>
                    )}
                    
                    {localStorage.getItem('token') && flights.length > 0 && (
                        <button
                            onClick={() => setShowSaveModal(true)}
                            className="save-search-button"
                        >
                            Save Search
                        </button>
                    )}
                </>
            )}

            {showSaveModal && searchData && (
                <SaveSearchModal
                    searchData={{
                        origin: searchData.origin,
                        destination: searchData.destination,
                        originIata: searchData.originIata,
                        destinationIata: searchData.destinationIata,
                        departureDate: searchData.departureDate,
                        returnDate: searchData.returnDate
                    }}
                    onClose={() => setShowSaveModal(false)}
                />
            )}
        </div>
    );
};

export default FlightSearchPage;