import { Link } from 'react-router-dom';

export default function Navbar() {
  return (
    <nav className="bg-black shadow-sm">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link to="/" className="text-xl font-bold text-sky-200">
          AI News Scraper
        </Link>
        <div className="flex gap-8 text-lg">
          <Link
            to="/"
            className="text-gray-100 hover:text-gray-400 transition-colors"
          >
            Home
          </Link>
          <Link
            to="/search"
            className="text-gray-100 hover:text-gray-400 transition-colors mr-5"
          >
            Search
          </Link>
        </div>
      </div>
    </nav>
  );
}