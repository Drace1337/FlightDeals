import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlane, faClock, faMoneyBillWave, faUser, faCalendarAlt } from '@fortawesome/free-solid-svg-icons';
import './FlightResults.scss';

const FlightResults = ({ flights, origin, destination }) => {
  if (!flights || flights.length === 0) {
    return (
      <div className="flight-results">
        <div className="no-flights">
          <p>No flights found for your search criteria.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flight-results">
      <h2 className="flight-results__title">
        Available Flights ({flights.length} found)
      </h2>
      <div className="flight-results__list">
        {flights.map((flight) => (
          <div key={flight.id} className="flight-card">
            <div className="flight-card__header">
              <div className="flight-card__airline-info">
                <span className="flight-card__airline">{flight.airline}</span>
                <span className="flight-card__flight-number">{flight.flightNumber}</span>
              </div>
              <div className="flight-card__price-info">
                <span className="flight-card__price">{flight.price}</span>
                <span className="flight-card__class">{flight.class}</span>
              </div>
            </div>
            
            <div className="flight-card__route">
              <div className="flight-card__segment">
                <div className="flight-card__airport">
                  <span className="flight-card__city">{flight.origin}</span>
                  <span className="flight-card__time">{flight.departureTime}</span>
                </div>
                
                <div className="flight-card__flight-info">
                  <FontAwesomeIcon icon={faPlane} className="flight-card__icon" />
                  <span className="flight-card__duration">{flight.duration}</span>
                  {flight.stops > 0 && (
                    <span className="flight-card__stops">{flight.stops} stop{flight.stops > 1 ? 's' : ''}</span>
                  )}
                </div>
                
                <div className="flight-card__airport">
                  <span className="flight-card__city">{flight.destination}</span>
                  <span className="flight-card__time">{flight.arrivalTime}</span>
                </div>
              </div>
              
              {flight.hasReturn && flight.returnInfo && (
                <div className="flight-card__return">
                  <div className="flight-card__return-label">Return Flight</div>
                  <div className="flight-card__segment">
                    <div className="flight-card__airport">
                      <span className="flight-card__city">{flight.destination}</span>
                      <span className="flight-card__time">{flight.returnInfo.departureTime}</span>
                    </div>
                    
                    <div className="flight-card__flight-info">
                      <FontAwesomeIcon icon={faPlane} className="flight-card__icon flight-card__icon--return" />
                      <span className="flight-card__duration">{flight.returnInfo.duration}</span>
                    </div>
                    
                    <div className="flight-card__airport">
                      <span className="flight-card__city">{flight.origin}</span>
                      <span className="flight-card__time">{flight.returnInfo.arrivalTime}</span>
                    </div>
                  </div>
                  <div className="flight-card__return-flight-number">
                    {flight.returnInfo.flightNumber}
                  </div>
                </div>
              )}
            </div>
            
            <div className="flight-card__details">
              <span className="flight-card__detail">
                <FontAwesomeIcon icon={faClock} /> {flight.duration}
              </span>
              <span className="flight-card__detail">
                <FontAwesomeIcon icon={faMoneyBillWave} /> {flight.class}
              </span>
              {flight.aircraft && (
                <span className="flight-card__detail">
                  Aircraft: {flight.aircraft}
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default FlightResults;