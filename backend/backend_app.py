from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Get all posts with optional sorting."""
    # Get query parameters for sorting
    sort_by = request.args.get('sort', '').lower()
    direction = request.args.get('direction', 'asc').lower()
    
    # Create a copy of POSTS to avoid modifying the original list
    posts = POSTS.copy()
    
    # If sort parameter is provided, validate and apply sorting
    if sort_by:
        # Validate sort parameter
        if sort_by not in ['title', 'content']:
            return jsonify({"error": "Invalid sort field. Allowed values are: 'title' or 'content'"}), 400
        
        # Validate direction parameter
        if direction not in ['asc', 'desc']:
            return jsonify({"error": "Invalid sort direction. Allowed values are: 'asc' or 'desc'"}), 400
        
        # Sort posts by the specified field
        posts.sort(key=lambda post: post[sort_by].lower(), reverse=(direction == 'desc'))
    
    return jsonify(posts)


@app.route('/api/posts', methods=['POST'])
def add_post():
    """Add a new blog post to the list."""
    # Get the JSON data from the request
    data = request.get_json()
    
    # Validate that title and content are provided
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "Missing required fields: title and content"}), 400
    
    # Generate a new unique ID (max ID + 1)
    new_id = max([post['id'] for post in POSTS]) + 1 if POSTS else 1
    
    # Create the new post
    new_post = {
        "id": new_id,
        "title": data['title'],
        "content": data['content']
    }
    
    # Add the post to the list
    POSTS.append(new_post)
    
    # Return the new post with 201 Created status code
    return jsonify(new_post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a blog post by its ID."""
    # Find the post with the given ID
    post = next((p for p in POSTS if p['id'] == post_id), None)
    
    # If the post doesn't exist, return 404
    if post is None:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404
    
    # Remove the post from the list
    POSTS.remove(post)
    
    # Return a success message with 200 OK status code
    return jsonify({"message": f"Post with id {post_id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """Update a blog post by its ID."""
    # Find the post with the given ID
    post = next((p for p in POSTS if p['id'] == post_id), None)
    
    # If the post doesn't exist, return 404
    if post is None:
        return jsonify({"error": f"Post with id {post_id} not found."}), 404
    
    # Get the JSON data from the request
    data = request.get_json()
    
    # Update title if provided, otherwise keep the old title
    if data and 'title' in data:
        post['title'] = data['title']
    
    # Update content if provided, otherwise keep the old content
    if data and 'content' in data:
        post['content'] = data['content']
    
    # Return the updated post with 200 OK status code
    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """Search for blog posts by title or content."""
    # Get query parameters from the URL
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()
    
    # Filter posts based on search criteria
    results = []
    for post in POSTS:
        # Check if title query matches (case-insensitive)
        title_match = title_query in post['title'].lower() if title_query else False
        # Check if content query matches (case-insensitive)
        content_match = content_query in post['content'].lower() if content_query else False
        
        # Add post to results if either title or content matches
        if title_match or content_match:
            results.append(post)
    
    # Return the search results
    return jsonify(results), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
