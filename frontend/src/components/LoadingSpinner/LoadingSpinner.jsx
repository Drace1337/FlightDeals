import './LoadingSpinner.scss';

const LoadingSpinner = () => (
  <div className="loading-spinner">
    <div className="spinner"></div>
    <p>Searching for flights...</p>
  </div>
);

export default LoadingSpinner;