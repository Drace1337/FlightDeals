import React, { useEffect, useState } from 'react';
import api from '../../services/api';
import './SearchHistoryPage.scss';

const SearchHistoryPage = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/history')
      .then(res => {
        setHistory(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="history-page">
      <h1>Your Search History</h1>
      
      {history.length === 0 ? (
        <p>No search history found</p>
      ) : (
        <div className="history-list">
          {history.map((item, index) => (
            <div key={index} className="history-item">
              <div className="history-item__route">
                <span>{item.origin} → {item.destination}</span>
              </div>
              <div className="history-item__dates">
                <span>{new Date(item.departure_date).toLocaleDateString()}</span>
                {item.return_date && (
                  <span> - {new Date(item.return_date).toLocaleDateString()}</span>
                )}
              </div>
              <div className="history-item__actions">
                <button>Search Again</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SearchHistoryPage;