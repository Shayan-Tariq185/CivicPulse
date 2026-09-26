import { Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import SubmitPage from './pages/SubmitPage';
import DashboardPage from './pages/DashboardPage';
import StatsPage from './pages/StatsPage';

export default function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Navigate to="/submit" replace />} />
        <Route path="/submit" element={<SubmitPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/stats" element={<StatsPage />} />
        {/* Catch-all */}
        <Route path="*" element={<Navigate to="/submit" replace />} />
      </Routes>
    </>
  );
}
