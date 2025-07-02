import React, { useState } from 'react';
import api from '../../services/api';
import SearchForm from '../../components/FlightSearch/SearchForm/SearchForm';
import AirportSelect from '../../components/FlightSearch/AirportSelect/AirportSelect';
import FlightResults from '../../components/FlightSearch/FlightResults/FlightResults';
import SaveSearchModal from '../../components/FlightSearch/SaveSearchModal/SaveSearchModal';
import './HomePage.scss';

const HomePage = () => {
  const [step, setStep] = useState(1); // 1: Form, 2: Airport select, 3: Results
  const [searchData, setSearchData] = useState(null);
  const [selectedAirports, setSelectedAirports] = useState({ origin: '', destination: '' });
  const [flights, setFlights] = useState([]);
  const [showSaveModal, setShowSaveModal] = useState(false);

  const handleSearchSubmit = (data) => {
    setSearchData(data);
    setStep(2);
  };

  const handleAirportSelect = (type, iata) => {
    setSelectedAirports(prev => ({ ...prev, [type]: iata }));
  };

  const handleFlightSearch = () => {
    api.get('/search/flights', {
      params: {
        origin_iata: selectedAirports.origin,
        destination_iata: selectedAirports.destination,
        departure_date: searchData.departureDate,
        return_date: searchData.returnDate,
        adults: searchData.adults
      }
    })
    .then(res => {
      setFlights(res.data);
      setStep(3);
    });
  };

  return (
    <div className="home-page">
      {step === 1 && <SearchForm onSubmit={handleSearchSubmit} />}
      
      {step === 2 && (
        <div className="airport-selection">
          <h2>Select Airports</h2>
          <AirportSelect 
            city={searchData.origin} 
            onSelect={(iata) => handleAirportSelect('origin', iata)} 
          />
          <AirportSelect 
            city={searchData.destination} 
            onSelect={(iata) => handleAirportSelect('destination', iata)} 
          />
          <button 
            onClick={handleFlightSearch}
            disabled={!selectedAirports.origin || !selectedAirports.destination}
          >
            Search Flights
          </button>
        </div>
      )}

      {step === 3 && (
        <>
          <FlightResults flights={flights} />
          {localStorage.getItem('token') && (
            <button onClick={() => setShowSaveModal(true)}>
              Save This Search
            </button>
          )}
        </>
      )}

      {showSaveModal && (
        <SaveSearchModal
          searchData={{ ...searchData, ...selectedAirports }}
          onClose={() => setShowSaveModal(false)}
        />
      )}
    </div>
  );
};

export default HomePage;