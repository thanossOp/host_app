from flask import Flask, request, jsonify, render_template, send_file
import pvorca
import json
import re
import pandas as pd

app = Flask(__name__)

orca = pvorca.create(
    access_key="89BlxJKCyiH/Eye4zhS74DxMibVpYlj/6qkLLw90NCm+ICw+AKYZqg=="
)

# Specify the path to your JSON file
json_file_path = "file.json"

# Open the JSON file and load its contents
with open(json_file_path, "r") as json_file:
    data = json.load(json_file)

# Dictionary to store user responses
user_responses = {}


def find_question_by_id(data, question_id):
    for item in data:
        if item["id"] == question_id:
            return item
    return None


def extract_numeric_value(user_input):
    numeric_values = []
    numeric_str = ""
    number_mapping = {
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
        "ten": "10",
    }

    for word in user_input.lower().split():
        if word.isdigit() or word.replace(".", "", 1).isdigit():
            numeric_str += word
        elif word in number_mapping:
            numeric_str += number_mapping[word]
        elif numeric_str:
            numeric_values.append(numeric_str)
            numeric_str = ""

    if numeric_str:
        numeric_values.append(numeric_str)
    if not numeric_values:
        return None
    try:
        last_sequence = numeric_values[-1]
        numeric_value = (
            float(last_sequence) if "." in last_sequence else int(last_sequence)
        )
        return numeric_value
    except ValueError:
        return None


def extract_job_title(user_input):
    file_path = "insurance_data.csv"

    original_df = pd.read_csv(file_path)
    job_titles = original_df["job_title"].unique()
    for job_title in job_titles:
        if job_title.lower() in user_input:
            return job_title

    return extract_job_title()


def number_to_words(num):
    # Define lists for ones, tens, and special cases up to 19
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    teens = [
        "ten",
        "eleven",
        "twelve",
        "thirteen",
        "fourteen",
        "fifteen",
        "sixteen",
        "seventeen",
        "eighteen",
        "nineteen",
    ]
    tens = [
        "",
        "",
        "twenty",
        "thirty",
        "forty",
        "fifty",
        "sixty",
        "seventy",
        "eighty",
        "ninety",
    ]

    # Define the magnitude names
    magnitudes = [
        "",
        "thousand",
        "million",
        "billion",
        "trillion",
        "quadrillion",
        "quintillion",
        "sextillion",
        "septillion",
        "octillion",
        "nonillion",
        "decillion",
    ]

    def convert_below_1000(n):
        if n == 0:
            return ""
        elif n < 10:
            return ones[n]
        elif n < 20:
            return teens[n - 10]
        elif n < 100:
            return tens[n // 10] + " " + convert_below_1000(n % 10)
        else:
            return ones[n // 100] + " hundred " + convert_below_1000(n % 100)

    if num == 0:
        return "zero"

    num_chunks = []
    while num:
        num_chunks.append(num % 1000)
        num //= 1000

    words_chunks = [
        convert_below_1000(chunk) + " " + magnitudes[i]
        for i, chunk in enumerate(num_chunks)
    ]
    words = " ".join(words_chunks[::-1])

    return words.strip()


def replace_numbers_with_words(input_text):
    numeric_values = re.findall(r"\b\d+\b", input_text)
    for num in numeric_values:
        num_as_text = number_to_words(int(num))
        input_text = input_text.replace(num, num_as_text)
    return input_text


def extract_name(input_text):
    matches_pattern = re.findall(r"my name is (\w+)", input_text, re.IGNORECASE)

    if matches_pattern:
        return matches_pattern[0]
    else:
        matches_words = re.findall(r"\b\w+\b", input_text)
        valid_names = [
            match
            for match in matches_words
            if match.lower() not in ["is", "my", "name"] and len(match) > 1
        ]

        if valid_names:
            return valid_names[0]
        else:
            return None


def extract_job_title(user_input):
    file_path = "insurance_data.csv"

    original_df = pd.read_csv(file_path)
    job_titles = original_df["job_title"].unique()
    for job_title in job_titles:
        if job_title.lower() in user_input:
            return job_title

    return extract_job_title()

def extract_binary_category(user_input):

    if "yes" in user_input or "no" in user_input:
        last_occurrence_yes = user_input.rfind("yes")
        last_occurrence_no = user_input.rfind("no")
        last_occurrence = max(last_occurrence_yes, last_occurrence_no)
        category_value = user_input[last_occurrence : last_occurrence + 3]
    else:
        return extract_binary_category()

    return category_value


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/jsonroute", methods=["POST"])
def get_audio():
    question_id = request.json.get("questionId")
    question = find_question_by_id(data, str(question_id))
    if question is None:
        return "Question not found", 404
    orca.synthesize_to_file(question["question"], "output.wav")
    initial_audio_file_path = "output.wav"
    return send_file(initial_audio_file_path, mimetype="audio/wav")


@app.route("/user-response", methods=["POST"])
def process_user_response():
    data = request.json
    question_id = data.get("questionId")
    user_response = data.get("response")
    user_responses[question_id] = user_response

    valid_response = validate_response(question_id, user_response)
    if valid_response:
        next_question_id = str(int(question_id) + 1)
        return jsonify({"nextQuestionId": next_question_id})
    else:
        return jsonify({"nextQuestionId": question_id})


def validate_response(question_id, response):
    if question_id == "2":
        age = extract_numeric_value(response)
        if age is None or age < 0 or age > 120:
            return False
    return True


@app.route("/generate-message", methods=["GET"])
def generate_message():
    user_name = user_responses.get("1", "")
    user_age = user_responses.get("2", "")
    # user_job = user_responses.get("3", "")
    # user_smoke = user_responses.get("4", "")
    # user_bp = user_responses.get("5", "")
    # user_re = user_responses.get("6", "")
    # job = extract_job_title(user_job)
    # smoke = extract_binary_category(user_smoke)
    # bp = extract_numeric_value(user_bp)
    # regular_exercise = extract_binary_category(user_re)
    age = extract_numeric_value(user_age)
    name = extract_name(user_name)
    message = f"Nice to meet you {name}.You are {age} years old."
    newmessage = replace_numbers_with_words(message)
    orca.synthesize_to_file(newmessage, "message.wav")
    audio_file_path = "message.wav"
    return send_file(audio_file_path, mimetype="audio/wav")


if __name__ == "__main__":
    app.run(debug=True)
