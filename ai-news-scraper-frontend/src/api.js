import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000', // Your FastAPI backend URL
});

export const getArticles = () => API.get('/articles');
export const searchArticles = (query, source) => API.get('/search/', { params: { q: query, source } });
export const scrapeSite = (siteName) => API.post(`/scrape/${siteName}`);
export const getAvailableSites = () => API.get('/sites/');