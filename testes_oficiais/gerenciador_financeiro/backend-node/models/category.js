const mongoose = require('mongoose');

const categorySchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    trim: true
  },
  type: {
    type: String,
    enum: ['income', 'expense'],
    required: true
  },
  color: {
    type: String,
    default: '#667eea'
  },
  icon: {
    type: String,
    default: '📁'
  }
}, {
  timestamps: true
});

module.exports = mongoose.model('Category', categorySchema);