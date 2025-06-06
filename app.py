from flask import Flask, request, jsonify, render_template
import cohere
import os

app = Flask(__name__)

# Set your Cohere API key (can also be passed as environment variable)
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "5Eyn2NUukJ5RDkfUSbh0sTLmZ5JhPkCYX6jCerxW")
co = cohere.Client(COHERE_API_KEY)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/learn", methods=["POST"])
def learn():
    data = request.get_json()
    topic = data.get("topic", "")

    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    prompt = f"""
    You are an educational assistant helping beginners learn about: "{topic}".

    Please complete the following 3 sections clearly, and DO NOT skip any of them:

    ---

    Summary:  
    Write a clear, beginner-friendly 3 to 5 sentence explanation of the topic.
    keep sentences short and simple and make sure each sentence starts in a new line.

    ---

    Practice Questions:  
    Write 3 simple, beginner-level and short questions to test understanding.
    Use this format:
    1. ...
    2. ...
    3. ...

    ---

    Resources:  
    Provide 3 real online learning resources, formatted exactly as:
    1. Wikipedia - https://en.wikipedia.org/wiki/<relevant_topic>
    2. YouTube Search - https://www.youtube.com/results?search_query={topic}
    3. Course - <real Coursera, tedX, or Khan Academy link>

    Do not generate anything after the 3rd resource.
    """

    try:
        response = co.chat(
            model="command-r",
            message=prompt,
            temperature=0.5,
            max_tokens=700
        )


        answer = response.text.strip()
        return jsonify({"topic": topic, "response": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
