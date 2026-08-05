import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api",
  headers: {
    'Content-Type': 'application/json',
  },
});

// Trigger repository analysis 
export const ingestRepository = async (repoUrl) => {
  const response = await api.post('/ingest', { repo_url: repoUrl });
  return response.data;  
};

// Active processing status and progress for a task
export const getTaskStatus = async (taskId) => {
  const response = await api.get(`/status/${taskId}`);
  return response.data;  
};

// Fetch parsed metadata and stats 
export const getRepositoryDetails = async (repoId) => {
  const response = await api.get(`/repository/${repoId}`);
  return response.data; 
};

// Send user question and receive AI response with repo context
export const sendChatMessage = async (repositoryId, question) => {
  const response = await api.post('/chat', {
    repository_id: repositoryId,
    question: question,
  });
  return response.data;  
};

export default api;