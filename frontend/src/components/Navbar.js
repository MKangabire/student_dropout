import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="bg-blue-600 p-4 shadow-md">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <Link to="/" className="text-white text-2xl font-bold">Dropout Prediction</Link>
        <div className="space-x-4">
          <Link to="/upload" className="text-white hover:text-blue-200 transition">Upload</Link>
          <Link to="/retrain" className="text-white hover:text-blue-200 transition">Retrain</Link>
          <Link to="/predict" className="text-white hover:text-blue-200 transition">Predict</Link>
          <Link to="/evaluate" className="text-white hover:text-blue-200 transition">Evaluate</Link>
          <Link to="/visualize" className="text-white hover:text-blue-200 transition">Visualize</Link>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;