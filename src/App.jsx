import React, { useState } from 'react';
import './App.css';

const MovieRecommender = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [movies, setMovies] = useState([]);
  const [error, setError] = useState('');
  const [expandedMovies, setExpandedMovies] = useState({});

  const searchMovies = async (query) => {
    if (!query.trim()) return;
    
    setLoading(true);
    setError('');
    
    try {
      const response = await fetch('http://localhost:8000/get-movies', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: query })
      });
      
      if (!response.ok) {
        throw new Error('Failed to fetch recommendations');
      }
      
      const data = await response.json();
      
      if (data.error) {
        setError(data.error);
        setMovies([]);
      } else {
        setMovies(data.movie_details || []);
        setExpandedMovies({});
      }
    } catch (err) {
      setError('Connection error. Make sure the backend server is running on port 8000.');
      setMovies([]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      searchMovies(searchQuery);
    }
  };

  const toggleExpanded = (index) => {
    setExpandedMovies(prev => ({
      ...prev,
      [index]: !prev[index]
    }));
  };

  const MovieCard = ({ movie, index }) => {
    const isExpanded = expandedMovies[index];
    
    return (
      <div className="movie-card">
        <div className="movie-content">
          {/* Movie Poster */}
          <div className="poster-container">
            {movie.poster_url && movie.poster_url !== 'N/A' ? (
              <img 
                src={movie.poster_url} 
                alt={movie.title}
                className="poster-image"
                onError={(e) => {
                  e.target.style.display = 'none';
                  e.target.nextSibling.style.display = 'flex';
                }}
              />
            ) : null}
            <div className="poster-placeholder" style={{display: movie.poster_url && movie.poster_url !== 'N/A' ? 'none' : 'flex'}}>
              <span className="film-icon">🎬</span>
            </div>
          </div>
          
          {/* Movie Title */}
          <h3 className="movie-title">
            {movie.title}
          </h3>
          
          {/* Basic Info */}
          <div className="basic-info">
            <div className="info-item">
              <span className="icon">📅</span>
              <span>{movie.year}</span>
            </div>
            {movie.imdb_rating !== 'N/A' && (
              <div className="info-item">
                <span className="icon">⭐</span>
                <span>{movie.imdb_rating}</span>
              </div>
            )}
          </div>
          
          {/* More Button */}
          <button
            onClick={() => toggleExpanded(index)}
            className="more-button"
          >
            {isExpanded ? 'Less' : 'More'}
            <span className="chevron">{isExpanded ? '▲' : '▼'}</span>
          </button>
          
          {/* Expanded Details */}
          {isExpanded && (
            <div className="expanded-details">
              <div className="detail-item">
                <span className="detail-icon">⏱️</span>
                <div>
                  <span className="detail-label">Duration: </span>
                  <span className="detail-value">{movie.runtime}</span>
                </div>
              </div>
              
              <div className="detail-item">
                <span className="detail-icon">🌍</span>
                <div>
                  <span className="detail-label">Language: </span>
                  <span className="detail-value">{movie.language}</span>
                </div>
              </div>
              
              <div className="detail-item">
                <span className="detail-icon">🎭</span>
                <div>
                  <span className="detail-label">Genre: </span>
                  <span className="detail-value">{movie.genre}</span>
                </div>
              </div>
              
              <div className="detail-item">
                <span className="detail-icon">🎬</span>
                <div>
                  <span className="detail-label">Director: </span>
                  <span className="detail-value">{movie.director}</span>
                </div>
              </div>
              
              <div className="detail-item">
                <span className="detail-icon">👥</span>
                <div>
                  <span className="detail-label">Actors: </span>
                  <span className="detail-value">{movie.actors}</span>
                </div>
              </div>
              
              <div className="plot-section">
                <span className="detail-label">Plot: </span>
                <p className="plot-text">{movie.plot}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="app">
      <div className="container">
        {/* Header */}
        <div className="header">
          <h1 className="main-title">
            🎬 PopcornPicks
          </h1>
          <p className="subtitle">
            Discover your next favorite movie
          </p>
        </div>

        {/* Search Box */}
        <div className="search-section">
          <div className="search-container">
            <div className="search-box">
              <span className="search-icon">🔍</span>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Enter your movie preference (e.g., 'action movies', 'Leonardo DiCaprio films', 'time travel stories')"
                className="search-input"
                disabled={loading}
              />
              {loading && (
                <div className="loading-spinner">⏳</div>
              )}
            </div>
          </div>
          
          {/* Example suggestions */}
          <div className="suggestions">
            <p className="suggestions-text">Try these examples:</p>
            <div className="suggestion-buttons">
              {['action movies', 'romantic comedies', 'Christopher Nolan movies', 'movies like The Matrix'].map((example) => (
                <button
                  key={example}
                  onClick={() => {
                    setSearchQuery(example);
                    searchMovies(example);
                  }}
                  className="suggestion-button"
                  disabled={loading}
                >
                  {example}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="error-container">
            <div className="error-message">
              ❌ {error}
            </div>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="loading-container">
            <div className="loading-spinner-large">⏳</div>
            <p className="loading-text">Finding perfect movies for you...</p>
          </div>
        )}

        {/* Movie Results */}
        {movies.length > 0 && !loading && (
          <div className="results-section">
            <h2 className="results-title">
              🎭 Recommended Movies
            </h2>
            <div className="movies-grid">
              {movies.map((movie, index) => (
                <MovieCard key={index} movie={movie} index={index} />
              ))}
            </div>
          </div>
        )}

        {/* Welcome State */}
        {movies.length === 0 && !loading && !error && (
          <div className="welcome-container">
            <div className="welcome-icon">🎬</div>
            <p className="welcome-text">
              Enter your movie preferences above to get personalized recommendations!
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default MovieRecommender;