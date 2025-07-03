import React, { useState } from 'react';
import FlightSearchForm from '../FlightSearchForm/FlightSearchForm';
import FlightDetailsForm from '../FlightDetailsForm/FlightDetailsForm';
import FlightResults from '../FlightResults/FlightResults';
import SaveSearchModal from '../SaveSearchModal/SaveSearchModal';
import api from '../../../services/api';
import './FlightSearchPage.scss';

const FlightSearchPage = () => {
    const [step, setStep] = useState(1);
    const [searchData, setSearchData] = useState(null);
    const [flights, setFlights] = useState([]);
    const [showSaveModal, setShowSaveModal] = useState(false);

    const handleCitiesSubmit = async ({ origin, destination }) => {
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
        }
    };

const handleSearchSubmit = async (details) => {
  try {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('Please login first');
    }

    const response = await api.get('/search/flights', {
      params: {
        origin_iata: details.originIata,
        destination_iata: details.destinationIata,
        departure_date: details.departureDate,
        return_date: details.returnDate || undefined,
        adults: details.adults
      },
      headers: {
        'Authorization': `Bearer ${token}`  // ← KLUCZOWA ZMIANA
      }
    });

    if (!response.data) {
      throw new Error('No flights found');
    }

    setFlights(response.data);
    setStep(3);
  } catch (error) {
    console.error('Search error:', error);
    alert(`Error: ${error.message}. Please try again.`);
  }
};

    return (
        <div className="flight-search-page">
            {step === 1 && <FlightSearchForm onSubmit={handleCitiesSubmit} />}
            {step === 2 && (
                <FlightDetailsForm
                    originAirports={searchData.originAirports}
                    destinationAirports={searchData.destinationAirports}
                    onSubmit={handleSearchSubmit}
                    onBack={() => setStep(1)}
                />
            )}
            {step === 3 && (
                <>
                    <FlightResults
                        flights={flights}
                        origin={searchData.origin}
                        destination={searchData.destination}
                    />
                    {localStorage.getItem('token') && (
                        <button
                            onClick={() => setShowSaveModal(true)}
                            className="save-search-button"
                        >
                            Save Search
                        </button>
                    )}
                </>
            )}

            {showSaveModal && (
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