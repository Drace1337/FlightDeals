import React, { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import LoginForm from '../../components/Auth/LoginForm/LoginForm';
import RegisterForm from '../../components/Auth/RegisterForm/RegisterForm';
import './AuthPage.scss';

const AuthPage = () => {
  const [searchParams] = useSearchParams();
  const [activeTab, setActiveTab] = useState(searchParams.get('tab') || 'login');

  return (
    <div className="auth-page">
      <div className="auth-page__tabs">
        <button
          className={`auth-page__tab ${activeTab === 'login' ? 'auth-page__tab--active' : ''}`}
          onClick={() => setActiveTab('login')}
        >
          Login
        </button>
        <button
          className={`auth-page__tab ${activeTab === 'register' ? 'auth-page__tab--active' : ''}`}
          onClick={() => setActiveTab('register')}
        >
          Register
        </button>
      </div>
      <div className="auth-page__content">
        {activeTab === 'login' ? <LoginForm /> : <RegisterForm />}
      </div>
    </div>
  );
};

export default AuthPage;