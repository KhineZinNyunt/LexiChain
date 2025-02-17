from collections import defaultdict
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
train_data = 'sentences.txt'

# ✅ Use defaultdict(list) to avoid the 'append' AttributeError
first_possible_words = defaultdict(int)
second_possible_words = defaultdict(list)
transitions = defaultdict(list)

def expandDict(dictionary: dict, key, value):
    """Ensures that the key exists and appends the value to the list."""
    if isinstance(dictionary, defaultdict) and not isinstance(dictionary[key], list):
        print(f"Converting {key} in dictionary to list")
        dictionary[key] = []  # Convert to list if not already
    dictionary[key].append(value)

def get_next_probability(given_list):
    """Converts a list into a probability distribution dictionary."""
    probability_dict = {}
    total = len(given_list)
    for item in given_list:
        probability_dict[item] = probability_dict.get(item, 0) + 1
    return {key: value / total for key, value in probability_dict.items()}

def trainMarkovModel():
    """Train the Markov Model using text data from train_data."""
    with open(train_data, 'r', encoding='utf-8') as file:
        for line in file:
            tokens = line.rstrip().lower().split()
            for i, token in enumerate(tokens):
                if i == 0:
                    first_possible_words[token] += 1  # Track first words
                else:
                    prev_token = tokens[i - 1]
                    if i == len(tokens) - 1:
                        expandDict(transitions, (prev_token, token), 'END')
                    if i == 1:
                        expandDict(second_possible_words, prev_token, token)
                    else:
                        prev_prev_token = tokens[i - 2]
                        expandDict(transitions, (prev_prev_token, prev_token), token)

    # Normalize first word probabilities
    total_first_words = sum(first_possible_words.values())
    for key in first_possible_words:
        first_possible_words[key] /= total_first_words

    # Convert word lists to probability distributions
    for key in second_possible_words:
        second_possible_words[key] = get_next_probability(second_possible_words[key])
    
    for key in transitions:
        transitions[key] = get_next_probability(transitions[key])

def next_word(tpl):
    """Predict the next word(s) based on input string or tuple."""
    if isinstance(tpl, str):  # Single word input
        return list(second_possible_words.get(tpl, {}).keys())
    elif isinstance(tpl, tuple):  # Two-word input
        return list(transitions.get(tpl, {}).keys())
    return []

# Train the model at startup
trainMarkovModel()
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



