import React, { useState } from 'react';
import Sidebar from '../components/Sidebar';
import { motion } from 'framer-motion';
import { uploadTrainData } from '../services/api';

function UploadPage() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');
  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    if (!file) {
      setMessage('Please select a CSV file.');
      return;
    }
    setIsUploading(true);
    try {
      const response = await uploadTrainData(file);
      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Upload failed.');
    } finally {
      setIsUploading(false);
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
        <div className="bg-glass-bg backdrop-blur-md p-8 rounded-xl shadow-2xl max-w-lg w-full text-white border border-glass-border">
          <h2 className="text-2xl font-bold text-white mb-4">Upload Training Data</h2>
          <p className="text-gray-200 mb-4">
            Upload a CSV with 34 columns.{' '}
            <a href="/sample.csv" download className="text-blue-300 hover:underline">
              Download sample
            </a>
          </p>
          <input
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            disabled={isUploading}
            className="mb-4 w-full text-gray-200 bg-gray-800 bg-opacity-50 border border-gray-700 rounded-lg p-2"
          />
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleUpload}
            disabled={isUploading}
            className={`w-full py-3 px-4 rounded-full text-white ${isUploading ? 'bg-gray-500' : 'bg-blue-500 hover:bg-blue-600'} transition-all`}
          >
            {isUploading ? 'Uploading...' : 'Upload'}
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

export default UploadPage;