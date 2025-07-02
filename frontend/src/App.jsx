import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage/HomePage';
import AuthPage from './pages/AuthPage/AuthPage';
import ProfilePage from './pages/ProfilePage/ProfilePage';
import SearchHistoryPage from './pages/SearchHistoryPage/SearchHistoryPage';
import Header from './components/Navigation/Header/Header';
import PrivateRoute from './components/Navigation/PrivateRoute/PrivateRoute';
import './styles/main.scss';

function App() {
  return (
    <BrowserRouter>
      <Header />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/auth" element={<AuthPage />} />
          <Route path="/profile" element={<PrivateRoute><ProfilePage /></PrivateRoute>} />
          <Route path="/history" element={<PrivateRoute><SearchHistoryPage /></PrivateRoute>} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;