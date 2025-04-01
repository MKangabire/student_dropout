import React, { useState } from 'react';
import Sidebar from '../components/Sidebar';
import { motion } from 'framer-motion';
import { retrainModel } from '../services/api';

function RetrainPage() {
  const [message, setMessage] = useState('');
  const [isRetraining, setIsRetraining] = useState(false);

  const handleRetrain = async () => {
    setIsRetraining(true);
    try {
      const response = await retrainModel();
      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Retraining failed.');
    } finally {
      setIsRetraining(false);
    }
  };

  return (
    <div className="min-h-screen flex">
      <Sidebar />
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="flex-1 flex items-center justify-center p-6 ml-64"
      >
        <div className="bg-glass-bg backdrop-blur-md p-8 rounded-xl shadow-2xl max-w-md w-full text-white border border-glass-border">
          <h2 className="text-2xl font-bold text-white mb-4">Retrain Model</h2>
          <p className="text-gray-200 mb-4">Retrain the model with the latest data.</p>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleRetrain}
            disabled={isRetraining}
            className={`w-full py-3 px-4 rounded-full text-white ${isRetraining ? 'bg-gray-500' : 'bg-blue-500 hover:bg-blue-600'} transition-all`}
          >
            {isRetraining ? 'Retraining...' : 'Retrain'}
          </motion.button>
          {message && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className={`mt-4 text-center ${message.includes('success') ? 'text-green-400' : 'text-red-400'}`}
            >
              {message}
            </motion.p>
          )}
        </div>
      </motion.div>
    </div>
  );
}

export default RetrainPage;