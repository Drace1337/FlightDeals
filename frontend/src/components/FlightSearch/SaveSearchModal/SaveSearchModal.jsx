import React from 'react';
import api from '../../../services/api';
import './SaveSearchModal.scss';

const SaveSearchModal = ({ searchData, onClose }) => {
  const handleSave = async () => {
    try {
      await api.post('/search/save', {
        origin: searchData.origin,
        destination: searchData.destination,
        originIata: searchData.originIata,
        destinationIata: searchData.destinationIata,
        departure_date: searchData.departureDate,
        return_date: searchData.returnDate
      });
      onClose();
    } catch (error) {
      console.error('Error saving search:', error);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="save-modal">
        <h3>Save This Search</h3>
        <div className="search-info">
          <p><strong>Route:</strong> {searchData.origin} ({searchData.originIata}) → {searchData.destination} ({searchData.destinationIata})</p>
          <p><strong>Dates:</strong> {searchData.departureDate} to {searchData.returnDate || 'One-way'}</p>
        </div>
        <div className="modal-actions">
          <button onClick={onClose} className="cancel-button">
            Cancel
          </button>
          <button onClick={handleSave} className="save-button">
            Save
          </button>
        </div>
      </div>
    </div>
  );
};

export default SaveSearchModal;