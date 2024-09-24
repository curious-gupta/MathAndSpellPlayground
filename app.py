from flask import Flask, request, jsonify
from flask_cors import CORS
import random
from collections import defaultdict

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load words from a text file
def load_words(filename):
    words_by_letter = defaultdict(list)
    with open(filename, 'r') as file:
        for line in file:
            word = line.strip().lower()
            if 3 <= len(word) <= 6:  # Filter by word length
                words_by_letter[word[0]].append(word)
    return words_by_letter

words_by_letter = load_words('words.txt')

# Function to suggest easy spellings with variability in starting letters
def suggest_easy_spellings(number_of_spellings):
    starting_letters = list(words_by_letter.keys())
    if number_of_spellings > len(starting_letters):
        number_of_spellings = len(starting_letters)

    selected_letters = random.sample(starting_letters, number_of_spellings)
    selected_words = []
    for letter in selected_letters:
        selected_words.append(random.choice(words_by_letter[letter]))

    return selected_words

@app.route('/problems', methods=['GET'])
def get_problems():
    num_of_additions = int(request.args.get('num_of_additions', 5))
    num_of_subtractions = int(request.args.get('num_of_subtractions', 5))
    number_of_digits = int(request.args.get('number_of_digits', 6))

    addition_problems = [generate_addition_problem(number_of_digits) for _ in range(num_of_additions)]
    subtraction_problems = [generate_subtraction_problem(number_of_digits) for _ in range(num_of_subtractions)]

    problems = addition_problems + subtraction_problems

    return jsonify({"results": problems})

@app.route('/spellings', methods=['GET'])
def get_spellings():
    number_of_spellings = int(request.args.get('number_of_spellings', 5))

    spellings = suggest_easy_spellings(number_of_spellings)

    return jsonify({"spellings": spellings})

def generate_addition_problem(number_of_digits):
    lower_bound = 10**(number_of_digits - 1)
    upper_bound = (10**number_of_digits) - 1
    a = random.randint(lower_bound, upper_bound)
    b = random.randint(lower_bound, upper_bound)
    result = a + b
    return {
        "num1": str(a),
        "num2": str(b),
        "operation": "addition",
        "result": str(result)
    }

def generate_subtraction_problem(number_of_digits):
    lower_bound = 10**(number_of_digits - 1)
    upper_bound = (10**number_of_digits) - 1
    a = random.randint(lower_bound, upper_bound)
    b = random.randint(lower_bound, a - 1)  # Ensuring b is less than a for valid subtraction
    result = a - b
    return {
        "num1": str(a),
        "num2": str(b),
        "operation": "subtraction",
        "result": str(result)
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Ensure the port matches the one in your HTML
