import { useState } from 'react';
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline';

export default function SearchBar({ onSearch }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit} className="w-full flex justify-center mb-8">
  <div className="flex gap-[10px] items-center w-full max-w-3xl px-4">
    <input
      type="text"
      placeholder="Search articles..."
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      className="flex-grow px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
    />
    <button
      type="submit"
      className="px-6 py-2 bg-gray-950 text-white rounded-lg hover:bg-gray-400 transition-colors flex items-center gap-2"
    >
      <MagnifyingGlassIcon className="h-5 w-5" />
      Search
    </button>
  </div>
</form>

  );
}