from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your movie recommender class
try:
    from final_sample import MovieRecommender
    print("✅ Successfully imported MovieRecommender")
except ImportError as e:
    print(f"❌ Error importing MovieRecommender: {e}")
    print("Make sure 'final_sample.py' is in the same directory as this server.py")
    sys.exit(1)

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

# Initialize the movie recommender
try:
    recommender = MovieRecommender()
    print("✅ MovieRecommender initialized successfully")
except Exception as e:
    print(f"❌ Error initializing MovieRecommender: {e}")
    sys.exit(1)

@app.route('/get-movies', methods=['POST'])
def get_movies():
    """
    Get movie recommendations based on user input
    
    Expected JSON payload:
    {
        "text": "user movie preference"
    }
    
    Returns:
    {
        "user_input": "original input",
        "movie_names": ["movie1", "movie2", ...],
        "poster_urls": ["url1", "url2", ...],
        "movie_details": [{"title": "...", "year": "...", ...}, ...],
        "error": null or "error message"
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        user_input = data.get('text', '').strip()
        
        if not user_input:
            return jsonify({'error': 'No input text provided'}), 400
        
        print(f"🎬 Processing request for: '{user_input}'")
        
        # Get movie recommendations using your existing code
        result = recommender.get_complete_movie_data(user_input)
        
        print(f"✅ Found {len(result.get('movie_names', []))} movies")
        
        return jsonify(result)
    
    except Exception as e:
        error_message = f"Server error: {str(e)}"
        print(f"❌ {error_message}")
        return jsonify({'error': error_message}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'Backend is running!',
        'message': '🎬 Movie Recommender API is healthy',
        'endpoints': {
            '/get-movies': 'POST - Get movie recommendations',
            '/health': 'GET - Health check'
        }
    })

@app.route('/', methods=['GET'])
def home():
    """Root endpoint with API information"""
    return jsonify({
        'message': '🎬 Movie Recommender API',
        'version': '1.0.0',
        'endpoints': {
            '/get-movies': {
                'method': 'POST',
                'description': 'Get movie recommendations',
                'payload': {
                    'text': 'Your movie preference (e.g., "action movies", "Leonardo DiCaprio films")'
                }
            },
            '/health': {
                'method': 'GET', 
                'description': 'Health check'
            }
        },
        'example_request': {
            'url': 'http://localhost:8000/get-movies',
            'method': 'POST',
            'headers': {'Content-Type': 'application/json'},
            'body': {'text': 'action movies'}
        }
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'Available endpoints: /, /health, /get-movies'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong on the server'
    }), 500

if __name__ == '__main__':
    print("🎬 Movie Recommender Backend Starting...")
    print("=" * 50)
    print("📡 Server URL: http://localhost:8000")
    print("🔗 Frontend should connect to this URL")
    print("🏥 Health check: http://localhost:8000/health")
    print("📚 API info: http://localhost:8000/")
    print("=" * 50)
    print("🚀 Starting Flask server...")
    
    try:
        app.run(
            debug=True,          # Enable debug mode for development
            host='0.0.0.0',      # Accept connections from any IP
            port=8000,           # Run on port 8000
            threaded=True        # Enable threading for better performance
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        print("Make sure port 8000 is not already in use")