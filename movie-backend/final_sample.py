import http.client
import json
import urllib.parse
import time

class MovieRecommender:
    def __init__(self):
        # Built-in API keys
        self.GEMINI_API_KEY = "YOUR API KEY"
        self.OMDB_API_KEY = "YOUR API KEY"
    
    def get_movie_recommendations(self, user_input):
        """Get 5 movie recommendations based on user input using Gemini AI"""
        
        prompt = f"""Based on the following input: "{user_input}"

Please recommend exactly 5 movies. Analyze the input and provide relevant movie recommendations.

Format your response exactly like this (movie title only, no year or description):
1. Movie Title
2. Movie Title  
3. Movie Title
4. Movie Title
5. Movie Title

Only provide the 5 numbered movie titles, nothing else."""
        
        try:
            conn = http.client.HTTPSConnection('generativelanguage.googleapis.com')
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.8,
                    "maxOutputTokens": 500,
                    "topP": 0.9,
                    "topK": 20
                }
            }
            
            json_payload = json.dumps(payload)
            headers = {'Content-Type': 'application/json'}
            endpoint = f'/v1beta/models/gemini-1.5-flash-latest:generateContent?key={self.GEMINI_API_KEY}'
            
            conn.request('POST', endpoint, json_payload, headers)
            res = conn.getresponse()
            data = res.read()
            
            if res.status == 200:
                json_data = json.loads(data.decode('utf-8'))
                
                if 'candidates' in json_data and json_data['candidates']:
                    content = json_data['candidates'][0]['content']['parts'][0]['text']
                    return self.parse_movie_titles(content)
                else:
                    return ["Error: No recommendations found"]
                    
            else:
                return ["Error: API request failed"]
                
        except Exception as e:
            return [f"Error: {str(e)}"]
        finally:
            if 'conn' in locals():
                conn.close()
    
    def parse_movie_titles(self, content):
        """Extract clean movie titles from AI response"""
        lines = content.strip().split('\n')
        movies = []
        
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('•') or line.startswith('-')):
                # Remove numbering and clean up
                cleaned_line = line
                for prefix in ['1. ', '2. ', '3. ', '4. ', '5. ', '• ', '- ', '* ']:
                    if cleaned_line.startswith(prefix):
                        cleaned_line = cleaned_line[len(prefix):].strip()
                        break
                
                # Remove any parentheses and extra content
                if '(' in cleaned_line:
                    cleaned_line = cleaned_line.split('(')[0].strip()
                if '-' in cleaned_line:
                    cleaned_line = cleaned_line.split('-')[0].strip()
                
                if cleaned_line:
                    movies.append(cleaned_line)
        
        return movies[:5]
    
    def get_movie_details(self, movie_name):
        """Get detailed movie information from OMDb API"""
        try:
            conn = http.client.HTTPSConnection('www.omdbapi.com')
            encoded_movie = urllib.parse.quote(movie_name)
            endpoint = f'/?t={encoded_movie}&apikey={self.OMDB_API_KEY}'
            
            conn.request('GET', endpoint)
            res = conn.getresponse()
            data = res.read()
            
            if res.status == 200:
                json_data = json.loads(data.decode('utf-8'))
                
                if json_data.get('Response') == 'True':
                    return {
                        'title': json_data.get('Title', 'N/A'),
                        'year': json_data.get('Year', 'N/A'),
                        'genre': json_data.get('Genre', 'N/A'),
                        'director': json_data.get('Director', 'N/A'),
                        'actors': json_data.get('Actors', 'N/A'),
                        'plot': json_data.get('Plot', 'N/A'),
                        'poster_url': json_data.get('Poster', 'N/A'),
                        'imdb_rating': json_data.get('imdbRating', 'N/A'),
                        'runtime': json_data.get('Runtime', 'N/A'),
                        'language': json_data.get('Language', 'N/A'),
                        'country': json_data.get('Country', 'N/A')
                    }
                else:
                    return None
            else:
                return None
                
        except Exception as e:
            return None
        finally:
            if 'conn' in locals():
                conn.close()
    
    def get_complete_movie_data(self, user_input):
        """
        Get complete movie data: recommendations with posters and details
        
        Returns:
            dict: Complete movie data with separate variables
        """
        print(f"🤖 Getting movie recommendations for: '{user_input}'...")
        
        # Get movie recommendations
        movie_titles = self.get_movie_recommendations(user_input)
        
        if not movie_titles or movie_titles[0].startswith('Error'):
            return {
                'user_input': user_input,
                'movie_names': [],
                'poster_urls': [],
                'movie_details': [],
                'error': 'Failed to get recommendations'
            }
        
        print("📽️  Found movies, getting details and posters...")
        
        movie_names = []
        poster_urls = []
        movie_details = []
        
        for i, movie_title in enumerate(movie_titles, 1):
            print(f"   {i}/5 Processing: {movie_title}")
            
            # Get detailed movie info
            details = self.get_movie_details(movie_title)
            
            if details:
                movie_names.append(details['title'])
                poster_urls.append(details['poster_url'] if details['poster_url'] != 'N/A' else None)
                movie_details.append(details)
            else:
                movie_names.append(movie_title)
                poster_urls.append(None)
                movie_details.append({
                    'title': movie_title,
                    'year': 'N/A',
                    'genre': 'N/A',
                    'director': 'N/A',
                    'actors': 'N/A',
                    'plot': 'Details not available',
                    'poster_url': 'N/A',
                    'imdb_rating': 'N/A',
                    'runtime': 'N/A',
                    'language': 'N/A',
                    'country': 'N/A'
                })
            
            # Small delay to be respectful to APIs
            time.sleep(0.5)
        
        return {
            'user_input': user_input,
            'movie_names': movie_names,
            'poster_urls': poster_urls,
            'movie_details': movie_details,
            'error': None
        }
    
    def display_results(self, data):
        """Display the complete movie results"""
        if data['error']:
            print(f"❌ Error: {data['error']}")
            return
        
        print(f"\n🎬 Movie Recommendations for: '{data['user_input']}'")
        print("=" * 60)
        
        for i, (name, poster, details) in enumerate(zip(data['movie_names'], data['poster_urls'], data['movie_details']), 1):
            print(f"\n{i}. 🎭 {name}")
            print(f"   📅 Year: {details['year']}")
            print(f"   🎪 Genre: {details['genre']}")
            print(f"   🎬 Director: {details['director']}")
            print(f"   ⭐ IMDb Rating: {details['imdb_rating']}")
            print(f"   ⏱️  Runtime: {details['runtime']}")
            print(f"   🌍 Language: {details['language']}")
            print(f"   📝 Plot: {details['plot'][:100]}{'...' if len(details['plot']) > 100 else ''}")
            
            if poster and poster != 'N/A':
                print(f"   🖼️  Poster: {poster}")
            else:
                print(f"   🖼️  Poster: Not available")
            print(f"   {'-' * 50}")

def main():
    """Main interactive function"""
    recommender = MovieRecommender()
    
    print("🎬 AI Movie Recommender with Posters")
    print("=" * 50)
    print("Examples you can try:")
    print("• 'action movies'")
    print("• 'Leonardo DiCaprio films'") 
    print("• 'time travel stories'")
    print("• 'romantic comedies'")
    print("• 'movies like The Matrix'")
    print("• 'Christopher Nolan movies'")
    print("• Or literally anything else!")
    print("=" * 50)
    
    while True:
        user_input = input("\n🎯 Enter your movie preference (or 'quit' to exit): ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("🎬 Thanks for using Movie Recommender! Goodbye!")
            break
            
        if not user_input:
            print("❌ Please enter something!")
            continue
        
        # Get complete movie data
        movie_data = recommender.get_complete_movie_data(user_input)
        
        # Display results  
        recommender.display_results(movie_data)
        
        # Show separate variables for reference
        print(f"\n📊 DATA VARIABLES:")
        print(f"movie_names = {movie_data['movie_names']}")
        print(f"poster_urls = {movie_data['poster_urls']}")
        print(f"Total movies found: {len(movie_data['movie_names'])}")
        
        continue_search = input("\n🔄 Search again? (y/n): ").strip().lower()
        if continue_search not in ['y', 'yes']:
            print("🎬 Thanks for using Movie Recommender! Goodbye!")
            break

# Simple function for direct use
def get_movies_with_posters(text):
    """
    Simple function to get movie recommendations with posters
    
    Args:
        text (str): Any input text
    
    Returns:
        dict: Complete movie data
    """
    recommender = MovieRecommender()
    return recommender.get_complete_movie_data(text)

if __name__ == "__main__":
    main()
    
    # Example of direct usage:
    # result = get_movies_with_posters("sci-fi movies")
    # print("Movie Names:", result['movie_names'])
    # print("Poster URLs:", result['poster_urls'])
    # print("Full Details:", result['movie_details'])
