import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const ingestRepository = async (repoUrl) => {
  const response = await api.post('/ingest', { repo_url: repoUrl });
  return response.data; // { task_id: string }
};

export const getTaskStatus = async (taskId) => {
  const response = await api.get(`/status/${taskId}`);
  return response.data; // { progress: number, status: string, ready: boolean, error: string }
};

export const getRepositoryDetails = async (repoId) => {
  const response = await api.get(`/repository/${repoId}`);
  return response.data; // { summary, languages, total_files, files, status }
};

export const sendChatMessage = async (repositoryId, question) => {
  const response = await api.post('/chat', {
    repository_id: repositoryId,
    question: question,
  });
  return response.data; // { answer: string, citations: Array }
};

export default api;