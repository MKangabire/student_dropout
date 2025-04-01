import React from 'react';
import Sidebar from '../components/Sidebar';
import { motion } from 'framer-motion';

function Home() {
  return (
    <div className="min-h-screen flex">
      <Sidebar />
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
        className="flex-1 flex items-center justify-center p-6 ml-64"
      >
        <div className="bg-glass-bg backdrop-blur-md p-8 rounded-xl shadow-2xl max-w-lg w-full text-center text-white border border-glass-border">
          <motion.h1
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="text-4xl font-extrabold mb-6"
          >
            Student Dropout Prediction
          </motion.h1>
          <motion.p
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="text-lg mb-8"
          >
            Leverage AI to predict student dropout risks with precision and insight.
          </motion.p>
          <motion.button
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            whileHover={{ scale: 1.05 }}
            className="bg-blue-500 text-white py-3 px-8 rounded-full hover:bg-blue-600 transition-all"
          >
            <a href="/predict">Start Predicting</a>
          </motion.button>
        </div>
      </motion.div>
    </div>
  );
}

export default Home;