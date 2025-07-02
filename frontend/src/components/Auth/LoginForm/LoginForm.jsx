import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../../services/api';
import './LoginForm.scss';

const LoginForm = () => {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post('/auth/login', formData);
      localStorage.setItem('token', res.data.access_token);
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.message || 'Login failed');
    }
  };

  return (
    <form className="auth-form" onSubmit={handleSubmit}>
      <h2 className="auth-form__title">Login</h2>
      {error && <p className="auth-form__error">{error}</p>}
      <div className="auth-form__group">
        <label className="auth-form__label">Email:</label>
        <input
          type="email"
          className="auth-form__input"
          value={formData.email}
          onChange={(e) => setFormData({...formData, email: e.target.value})}
          required
        />
      </div>
      <div className="auth-form__group">
        <label className="auth-form__label">Password:</label>
        <input
          type="password"
          className="auth-form__input"
          value={formData.password}
          onChange={(e) => setFormData({...formData, password: e.target.value})}
          required
        />
      </div>
      <button type="submit" className="auth-form__button">Login</button>
    </form>
  );
};

export default LoginForm;