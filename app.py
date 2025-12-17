from flask import Flask, render_template, request, jsonify
import logic 
import os
import time

app = Flask(__name__)

# 1. LANDING PAGE
@app.route('/')
def landing():
    return render_template('landing.html')

# 2. APP PAGE
@app.route('/app')
def generator_app():
    return render_template('index.html')

# 3. GENERATE ACTION
@app.route('/generate', methods=['POST'])
def generate():
    topic = request.form.get('topic')
    print(f"🔮 Genie received wish: {topic}")

    try:
        # Run the logic (Now handles subtitles internally)
        result = logic.make_reel(topic)

        # CHECK FOR ERRORS
        # If logic.py returns a string starting with "Error", something went wrong
        if result.startswith("Error"):
            return jsonify({
                "success": False,
                "error": result
            })
        
        # SUCCESS
        # We add a timestamp (?t=...) to the URL to prevent the browser 
        # from showing the cached OLD video instead of the new one.
        timestamp = int(time.time())
        video_url = f"/static/final_reel.mp4?t={timestamp}"

        return jsonify({
            "success": True,
            "video_url": video_url,
            "script": result
        })

    except Exception as e:
        print(f"❌ Server Error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        })

if __name__ == '__main__':
    # Ensure static folder exists
    if not os.path.exists('static'):
        os.makedirs('static')
    
    app.run(debug=True)