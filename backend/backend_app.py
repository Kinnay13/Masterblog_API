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
    return jsonify(POSTS)


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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
