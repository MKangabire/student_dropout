import React, { useState } from 'react';
import Sidebar from '../components/Sidebar';
import { motion } from 'framer-motion';
import { evaluateModel } from '../services/api';

function EvaluatePage() {
  const [metrics, setMetrics] = useState(null);
  const [isEvaluating, setIsEvaluating] = useState(false);

  const handleEvaluate = async () => {
    setIsEvaluating(true);
    try {
      const response = await evaluateModel();
      setMetrics(response.data);
    } catch (error) {
      setMetrics({ error: error.response?.data?.detail || 'Evaluation failed.' });
    } finally {
      setIsEvaluating(false);
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
        <div className="bg-glass-bg backdrop-blur-md p-8 rounded-xl shadow-2xl max-w-2xl w-full text-white border border-glass-border">
          <h2 className="text-2xl font-bold text-white mb-4">Evaluate Model</h2>
          <p className="text-gray-200 mb-4">Assess model performance on test data.</p>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleEvaluate}
            disabled={isEvaluating}
            className={`w-full py-3 px-4 rounded-full text-white ${isEvaluating ? 'bg-gray-500' : 'bg-blue-500 hover:bg-blue-600'} transition-all`}
          >
            {isEvaluating ? 'Evaluating...' : 'Evaluate'}
          </motion.button>
          {metrics && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="mt-6"
            >
              {metrics.error ? (
                <p className="text-red-400 text-center">{metrics.error}</p>
              ) : (
                <pre className="bg-gray-800 bg-opacity-50 p-4 rounded-lg text-sm text-gray-200 overflow-auto max-h-96">
                  {JSON.stringify(metrics, null, 2)}
                </pre>
              )}
            </motion.div>
          )}
        </div>
      </motion.div>
    </div>
  );
}

export default EvaluatePage;