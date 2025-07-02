import React from 'react';
import api from '../../../services/api';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlane, faClock, faMoneyBillWave } from '@fortawesome/free-solid-svg-icons';
import './FlightResults.scss';

const FlightResults = ({ flights }) => {
  if (!flights.length) return null;

  return (
    <div className="flight-results">
      <h2 className="flight-results__title">Available Flights</h2>
      <div className="flight-results__list">
        {flights.map((flight, index) => (
          <div key={index} className="flight-card">
            <div className="flight-card__header">
              <span className="flight-card__airline">{flight.airline}</span>
              <span className="flight-card__price">${flight.price}</span>
            </div>
            <div className="flight-card__route">
              <div className="flight-card__segment">
                <span className="flight-card__city">{flight.origin}</span>
                <FontAwesomeIcon icon={faPlane} className="flight-card__icon" />
                <span className="flight-card__city">{flight.destination}</span>
              </div>
              <div className="flight-card__details">
                <span className="flight-card__detail">
                  <FontAwesomeIcon icon={faClock} /> {flight.duration}
                </span>
                <span className="flight-card__detail">
                  <FontAwesomeIcon icon={faMoneyBillWave} /> {flight.class}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default FlightResults;