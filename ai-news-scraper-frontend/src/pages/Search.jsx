import { useState } from 'react';
import ArticleCard from '../components/ArticleCard';
import SearchBar from '../components/SearchBar';
import { searchArticles } from '../api';

export default function Search() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  

  const handleSearch = async (query, source) => {
    setLoading(true);
    try {
      const { data } = await searchArticles(query, source);
      setResults(data);
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-8 text-center">Search Articles</h1>
      <SearchBar onSearch={handleSearch} />
      
      {loading ? (
        <div className="text-center py-8">Searching...</div>
      ) : (
        <div className="grid gap-6">
          {results.map((article) => (
            <ArticleCard key={article.id} article={article} />
          ))}
          {results.length === 0 && (
            <p className="text-center text-gray-500">  Results are extracted from Science Daily and Wired AI</p>
          )}
        </div>
      )}
    </div>
  );
}