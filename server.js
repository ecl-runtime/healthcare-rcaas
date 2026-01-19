const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();

// COMMENT: Middleware
app.use(cors());
app.use(express.json());

// COMMENT: Basic route for health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'Server is running',
    timestamp: new Date(),
    ollama: 'http://localhost:11434'
  });
});

// COMMENT: Route to check Ollama
app.get('/api/ollama/status', async (req, res) => {
  try {
    const response = await fetch('http://localhost:11434/api/tags');
    const data = await response.json();
    res.json({ status: 'connected', models: data.models });
  } catch (error) {
    res.json({ status: 'error', message: error.message });
  }
});

// COMMENT: Basic hospital endpoint
app.post('/api/hospitals', (req, res) => {
  const { name, state, cfo_email } = req.body;
  res.json({ 
    message: 'Hospital registered',
    data: { name, state, cfo_email }
  });
});

// COMMENT: Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
  console.log(`✅ Ollama API: ${process.env.OLLAMA_API}`);
  console.log(`✅ Supabase: ${process.env.SUPABASE_URL}`);
});
