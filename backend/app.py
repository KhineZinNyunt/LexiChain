from flask import Flask, request, jsonify
from flask_cors import CORS
from markov import next_word, trainMarkovModel

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend interaction

# Re-train Markov model when server starts
trainMarkovModel()
@app.route('/')
def home():
    return "Flask API is working!"
@app.route('/suggest', methods=['GET'])
def suggest():
    input_text = request.args.get('input', '').strip().lower()
    words = input_text.split()

    if not words:
        return jsonify({'suggestions': []})

    suggestions = next_word(words[0]) if len(words) == 1 else next_word((words[-2], words[-1]))
    return jsonify({'suggestions': suggestions})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
# Define unique words in order
unique_words = ["I", "like", "machine", "learning", "books", "is", "fun", "reading"]

matrix = np.array([
    [0.00, 1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],  # I -> like
    [0.00, 0.00, 0.33, 0.00, 0.33, 0.00, 0.00, 0.33],  # like -> machine, books, reading
    [0.00, 0.00, 0.00, 1.00, 0.00, 0.00, 0.00, 0.00],  # machine -> learning
    [0.00, 0.00, 0.00, 0.00, 0.00, 1.00, 0.00, 0.00],  # learning -> is
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],  # books (no outgoing transitions)
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00, 0.00],  # is -> fun
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],  # fun (no outgoing transitions)
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],  # reading (no outgoing transitions)
])

# Create a DataFrame for visualization
df = pd.DataFrame(matrix, index=unique_words, columns=unique_words)

# Plot the heatmap
plt.figure(figsize=(8, 6), facecolor="gray")
sns.heatmap(df, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title("Word Transition Probability Matrix")
plt.xlabel("Next Word")
plt.ylabel("Current Word")
plt.show()



