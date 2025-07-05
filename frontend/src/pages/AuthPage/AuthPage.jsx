import React, { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import LoginForm from '../../components/Auth/LoginForm/LoginForm';
import RegisterForm from '../../components/Auth/RegisterForm/RegisterForm';
import './AuthPage.scss';
import { useNavigate } from 'react-router-dom';

const AuthPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();
  const tab = searchParams.get('tab') || 'login';

  const handleChange = (newTab) => {
    setSearchParams({ tab: newTab })
  }

  return (
    <div className="auth-page">
      <div className="auth-page__tabs">
        <button
          className={`auth-page__tab ${tab === 'login' ? 'auth-page__tab--active' : ''}`}
          onClick={() => handleChange('login')}
        >
          Login
        </button>
        <button
          className={`auth-page__tab ${tab === 'register' ? 'auth-page__tab--active' : ''}`}
          onClick={() => handleChange('register')}
        >
          Register
        </button>
      </div>
      <div className="auth-page__content">
        {tab === 'login' ? <LoginForm /> : <RegisterForm />}
      </div>
    </div>
  );
};

export default AuthPage;