import React, { useState } from 'react';
import Sidebar from '../components/Sidebar';
import { motion } from 'framer-motion';
import { makePrediction } from '../services/api';
import { Tooltip } from 'react-tooltip';

function PredictPage() {
  const [formData, setFormData] = useState({
    School: '', Mother_Education: '', Father_Education: '', Final_Grade: '',
    Grade_1: '', Grade_2: '', Number_of_Failures: '', Wants_Higher_Education: '',
    Study_Time: '', Weekend_Alcohol_Consumption: '', Weekday_Alcohol_Consumption: '',
    Address: '', Reason_for_Choosing_School: '',
  });
  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const response = await makePrediction(formData);
      setPrediction(response.data.prediction === 1 ? 'Will drop out' : 'Will not drop out');
    } catch (error) {
      setPrediction(error.response?.data?.detail || 'Prediction failed.');
    } finally {
      setIsLoading(false);
    }
  };

  const featureDescriptions = {
    School: 'Name of the school (e.g., MS).',
    Mother_Education: 'Mother’s education level (0-4: 0 = none, 4 = higher).',
    Father_Education: 'Father’s education level (0-4: 0 = none, 4 = higher).',
    Final_Grade: 'Final grade (0-20).',
    Grade_1: 'First assessment grade (0-20).',
    Grade_2: 'Second assessment grade (0-20).',
    Number_of_Failures: 'Past class failures (0-4).',
    Wants_Higher_Education: 'Pursue higher education? (yes/no).',
    Study_Time: 'Weekly study hours (1-4: 1 = <2h, 4 = >10h).',
    Weekend_Alcohol_Consumption: 'Weekend alcohol use (1-5: 1 = low, 5 = high).',
    Weekday_Alcohol_Consumption: 'Weekday alcohol use (1-5: 1 = low, 5 = high).',
    Address: 'Residence type (U = urban, R = rural).',
    Reason_for_Choosing_School: 'Reason for school choice (e.g., course).',
  };

  return (
    <div className="min-h-screen flex">
      <Sidebar />
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="flex-1 flex items-center justify-center p-6 ml-64"
      >
        <div className="bg-glass-bg backdrop-blur-md p-8 rounded-xl shadow-2xl max-w-4xl w-full text-white border border-glass-border">
          <h2 className="text-2xl font-bold text-white mb-6">Make a Prediction</h2>
          <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {Object.entries(featureDescriptions).map(([feature, desc]) => (
              <motion.div
                key={feature}
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.1 * Object.keys(featureDescriptions).indexOf(feature) }}
              >
                <label className="block text-gray-200 font-medium">
                  {feature.replace('_', ' ')}
                  <input
                    type={['Mother_Education', 'Father_Education', 'Final_Grade', 'Grade_1', 'Grade_2', 'Number_of_Failures', 'Study_Time', 'Weekend_Alcohol_Consumption', 'Weekday_Alcohol_Consumption'].includes(feature) ? 'number' : 'text'}
                    name={feature}
                    value={formData[feature]}
                    onChange={handleChange}
                    required
                    data-tooltip-id={feature}
                    data-tooltip-content={desc}
                    className="mt-1 block w-full p-3 bg-gray-800 bg-opacity-50 border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-white placeholder-gray-400"
                    placeholder={`Enter ${feature.replace('_', ' ')}`}
                  />
                  <Tooltip
                    id={feature}
                    place="top"
                    style={{ backgroundColor: '#1e40af', color: '#fff', padding: '8px', borderRadius: '4px' }}
                  />
                </label>
              </motion.div>
            ))}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              type="submit"
              disabled={isLoading}
              className={`col-span-full mt-6 py-3 px-4 rounded-full text-white ${isLoading ? 'bg-gray-500' : 'bg-blue-500 hover:bg-blue-600'} transition-all`}
            >
              {isLoading ? 'Predicting...' : 'Predict'}
            </motion.button>
          </form>
          {prediction && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className={`mt-6 text-center text-lg ${prediction.includes('failed') ? 'text-red-400' : 'text-green-400'}`}
            >
              Prediction: {prediction}
            </motion.p>
          )}
        </div>
      </motion.div>
    </div>
  );
}

export default PredictPage;