import React from 'react';
import './SaveSearchModal.scss';

const SaveSearchModal = ({ searchData, onClose }) => {
  const handleSave = () => {
    // Tutaj dodamy logikę zapisywania
    console.log('Zapisano wyszukiwanie:', searchData);
    onClose();
  };

  return (
    <div className="modal-overlay">
      <div className="save-modal">
        <h2 className="save-modal__title">Save Your Search</h2>
        
        <div className="save-modal__content">
          <div className="save-modal__route">
            <span>{searchData.origin} → {searchData.destination}</span>
          </div>
          <div className="save-modal__dates">
            <span>Departure: {searchData.departureDate}</span>
            {searchData.returnDate && (
              <span>Return: {searchData.returnDate}</span>
            )}
          </div>
        </div>

        <div className="save-modal__actions">
          <button 
            onClick={onClose}
            className="save-modal__button save-modal__button--cancel"
          >
            Cancel
          </button>
          <button 
            onClick={handleSave}
            className="save-modal__button save-modal__button--save"
          >
            Save Search
          </button>
        </div>
      </div>
    </div>
  );
};

export default SaveSearchModal;