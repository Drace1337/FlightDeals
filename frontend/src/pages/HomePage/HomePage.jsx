import React from 'react';
import FlightSearchPage from '../../components/FlightSearch/FlightSearchPage/FlightSearchPage';
import './HomePage.scss';

const HomePage = () => {
  return (
    <div className="home-page">
      <div className="home-page__container">
        <h1>Flight Search App</h1>
        <FlightSearchPage />
      </div>
    </div>
  );
};

export default HomePage;