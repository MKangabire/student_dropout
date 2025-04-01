import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

function Sidebar() {
  const navItems = [
    { to: '/', label: 'Home' },
    { to: '/upload', label: 'Upload' },
    { to: '/retrain', label: 'Retrain' },
    { to: '/predict', label: 'Predict' },
    { to: '/evaluate', label: 'Evaluate' },
    { to: '/visualize', label: 'Visualize' },
  ];

  return (
    <motion.div
      initial={{ x: -250 }}
      animate={{ x: 0 }}
      transition={{ duration: 0.5 }}
      className="fixed top-0 left-0 h-full w-64 bg-glass-bg backdrop-blur-md border-r border-glass-border text-white p-6 shadow-lg"
    >
      <h2 className="text-2xl font-bold mb-8">Dropout Prediction</h2>
      <nav>
        <ul className="space-y-4">
          {navItems.map((item) => (
            <li key={item.to}>
              <Link
                to={item.to}
                className="block py-2 px-4 rounded-lg hover:bg-blue-700 transition-all duration-300 transform hover:scale-105"
              >
                {item.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </motion.div>
  );
}

export default Sidebar;