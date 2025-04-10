export default function ArticleCard({ article }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-4 hover:shadow-lg transition-shadow">
      <h3 className="text-xl font-bold text-gray-800 mb-2">{article.title}</h3>
      <p className="text-gray-600 mb-3">{article.summary || 'No summary available'}</p>
      <div className="flex justify-between items-center">
        <span className="text-sm text-blue-600">{article.source}</span>
        <a 
          href={article.url} 
          target="_blank" 
          rel="noopener noreferrer"
          className="px-4 py-2 bg-gray-950 text-white rounded hover:bg-gray-400 transition-colors"
        >
          Read More
        </a>
      </div>
    </div>
  );
}