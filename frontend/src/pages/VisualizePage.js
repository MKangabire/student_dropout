import React, { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';
import { motion } from 'framer-motion';
import { getVisualization } from '../services/api';

function VisualizePage() {
  const [feature, setFeature] = useState('Grade_1');
  const [visualization, setVisualization] = useState(null);
  const [interpretation, setInterpretation] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const fetchVisualization = async (featureName) => {
    setIsLoading(true);
    try {
      const response = await getVisualization(featureName);
      setVisualization(response.data.image);
      setInterpretation(response.data.interpretation);
    } catch (error) {
      setVisualization(null);
      setInterpretation(error.response?.data?.detail || 'Failed to load visualization.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchVisualization(feature);
  }, [feature]);

  return (
    <div className="min-h-screen flex">
      <Sidebar />
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="flex-1 flex items-center justify-center p-6 ml-64"
      >
        <div className="bg-glass-bg backdrop-blur-md p-8 rounded-xl shadow-2xl max-w-4xl w-full text-white border border-glass-border">
          <h2 className="text-2xl font-bold text-white mb-4">Visualize Features</h2>
          <select
            value={feature}
            onChange={(e) => setFeature(e.target.value)}
            disabled={isLoading}
            className="w-full p-3 mb-6 bg-gray-800 bg-opacity-50 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="Grade_1">Grade 1</option>
            <option value="Study_Time">Study Time</option>
            <option value="Number_of_Failures">Number of Failures</option>
          </select>
          {isLoading ? (
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity }}
              className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full mx-auto"
            />
          ) : visualization ? (
            <motion.div initial={{ scale: 0.95 }} animate={{ scale: 1 }}>
              <img
                src={`data:image/png;base64,${visualization}`}
                alt={`${feature} Visualization`}
                className="w-full rounded-lg shadow-md"
              />
              <p className="mt-4 text-gray-200 text-center">{interpretation}</p>
            </motion.div>
          ) : (
            <p className="text-red-400 text-center">{interpretation}</p>
          )}
        </div>
      </motion.div>
    </div>
  );
}

export default VisualizePage;