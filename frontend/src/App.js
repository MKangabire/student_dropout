import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import UploadPage from './pages/UploadPage';
import RetrainPage from './pages/RetrainPage';
import PredictPage from './pages/PredictPage';
import EvaluatePage from './pages/EvaluatePage';
import VisualizePage from './pages/VisualizePage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<UploadPage />} />
        <Route path="/retrain" element={<RetrainPage />} />
        <Route path="/predict" element={<PredictPage />} />
        <Route path="/evaluate" element={<EvaluatePage />} />
        <Route path="/visualize" element={<VisualizePage />} />
      </Routes>
    </Router>
  );
}

export default App;