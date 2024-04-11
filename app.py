# import pandas as pd
# import speech_recognition as sr
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_absolute_error, r2_score
# from sklearn.impute import SimpleImputer
# import spacy
# import datetime
# import os
# import re
# import pvorca
# import pygame
# import time
# from flask import Flask, jsonify
# import pyttsx3

# app = Flask(__name__)

# current_session_file_path = None

# orca = pvorca.create(access_key='89BlxJKCyiH/Eye4zhS74DxMibVpYlj/6qkLLw90NCm+ICw+AKYZqg==')

# def log_interaction(log_text):
#     global current_session_file_path

#     if current_session_file_path is None:
#         timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#         folder_path = "data_recording"

#         if not os.path.exists(folder_path):
#             os.makedirs(folder_path)

#         current_session_file_path = os.path.join(
#             folder_path, f"interaction_log_{timestamp}.txt"
#         )

#     with open(current_session_file_path, "a") as log_file:
#         log_file.write(f"{log_text}\n")


# def restart_session():
#     global current_session_file_path
#     current_session_file_path = None


# def play_audio(filename):
#     pygame.mixer.init()
#     pygame.mixer.music.load(filename)
#     pygame.mixer.music.play()

#     while pygame.mixer.music.get_busy():
#         time.sleep(0.1)

#     pygame.mixer.quit()

#     os.remove(filename)


# def number_to_words(num):
#     # Define lists for ones, tens, and special cases up to 19
#     ones = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
#     teens = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
#     tens = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']

#     # Define the magnitude names
#     magnitudes = ['', 'thousand', 'million', 'billion', 'trillion', 'quadrillion', 'quintillion', 'sextillion', 'septillion', 'octillion', 'nonillion', 'decillion']

#     def convert_below_1000(n):
#         if n == 0:
#             return ''
#         elif n < 10:
#             return ones[n]
#         elif n < 20:
#             return teens[n - 10]
#         elif n < 100:
#             return tens[n // 10] + ' ' + convert_below_1000(n % 10)
#         else:
#             return ones[n // 100] + ' hundred ' + convert_below_1000(n % 100)

#     if num == 0:
#         return 'zero'

#     num_chunks = []
#     while num:
#         num_chunks.append(num % 1000)
#         num //= 1000

#     words_chunks = [convert_below_1000(chunk) + ' ' + magnitudes[i] for i, chunk in enumerate(num_chunks)]
#     words = ' '.join(words_chunks[::-1])  

#     return words.strip()
    
# def replace_numbers_with_words(input_text):
#     numeric_values = re.findall(r'\b\d+\b', input_text)
#     for num in numeric_values:
#         num_as_text = number_to_words(int(num))
#         input_text = input_text.replace(num, num_as_text)
#     return input_text


# def speak(response):
#     newText = replace_numbers_with_words(response)
    
#     orca.synthesize_to_file(newText,"output.wav")

#     play_audio("output.wav")
#     log_interaction(f"AI said: {newText}")


# def get_speech_input(try_count=0, max_tries=3):
#     if try_count > max_tries:
#         speak(
#             "It seems we're having trouble with the connection.I will call you latter. Goodbye!"
#         )
#         return None

#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         r.adjust_for_ambient_noise(source)
#         audio = r.listen(source, phrase_time_limit=10, timeout=10)

#     try:
#         user_input = r.recognize_google(audio)
#         log_interaction(f"User said: {user_input}\n")
#         return user_input.lower()
#     except sr.UnknownValueError as e:
#         print(e)
#         speak("I couldn't hear you")
#         return get_speech_input(try_count + 1, max_tries)


# def greet_user(user_name):

#     curent_hour = datetime.datetime.now().hour

#     if 5 < curent_hour < 12:
#         speak(f"Good Morning {user_name} , Welcome to our Health Insurance Planning System! To ensure I provide you with the best health insurance plan, I'll need some information. Your privacy is important, and all your information will be handled confidentially. Let's get started!")
#     elif 12 <= curent_hour < 18:
#         speak(f"Good Afternoon {user_name} , Welcome to our Health Insurance Planning System! To ensure I provide you with the best health insurance plan, I'll need some information. Your privacy is important, and all your information will be handled confidentially. Let's get started!")
#     else:
#         speak(f"Good Evening {user_name} , Welcome to our Health Insurance Planning System! To ensure I provide you with the best health insurance plan, I'll need some information. Your privacy is important, and all your information will be handled confidentially. Let's get started!")


# file_path = "insurance_data.csv"

# original_df = pd.read_csv(file_path)

# imputer = SimpleImputer(strategy="mean")

# column_with_missing_values = ["age"]

# original_df[column_with_missing_values] = imputer.fit_transform(
#     original_df[column_with_missing_values]
# )

# features = original_df.drop(["claim"], axis=1)
# target = original_df["claim"]


# categorical_columns = features.select_dtypes(include=["object"]).columns

# features = pd.get_dummies(features, columns=categorical_columns, drop_first=True)

# X_train, X_test, y_train, y_test = train_test_split(
#     features, target, test_size=0.2, random_state=42
# )

# reg = RandomForestRegressor(n_estimators=400, max_depth=4, random_state=42)
# reg.fit(X_train, y_train)


# def extract_gender():
#     user_input = get_speech_input().lower()

#     if "male" in user_input:
#         gender = "male"
#     elif "female" in user_input:
#         gender = "female"
#     else:
#         speak("Can't understand. Please provide valid gender (male or female).")
#         return extract_gender()

#     return gender


# def extract_numeric_value():
#     user_input = get_speech_input()

#     numeric_values = []
#     numeric_str = ""
#     number_mapping = {
#         "zero": "0",
#         "one": "1",
#         "two": "2",
#         "three": "3",
#         "four": "4",
#         "five": "5",
#         "six": "6",
#         "seven": "7",
#         "eight": "8",
#         "nine": "9",
#         "ten": "10",
#     }

#     for word in user_input.lower().split():
#         if word.isdigit() or word.replace(".", "", 1).isdigit():
#             numeric_str += word
#         elif word in number_mapping:
#             numeric_str += number_mapping[word]
#         elif numeric_str:
#             numeric_values.append(numeric_str)
#             numeric_str = ""

#     if numeric_str:
#         numeric_values.append(numeric_str)

#     try:
#         last_sequence = numeric_values[-1]
#         numeric_value = (
#             float(last_sequence) if "." in last_sequence else int(last_sequence)
#         )
#         return numeric_value
#     except ValueError:
#         speak(f"Sorry, I couldn't understand. Please provide a valid numeric value.")
#         return extract_numeric_value()
#     except IndexError:
#         speak(f"Sorry, I couldn't understand. Please provide a valid numeric value.")
#         return extract_numeric_value()


# def extract_binary_category():
#     user_input = get_speech_input().lower()

#     if "yes" in user_input or "no" in user_input:
#         last_occurrence_yes = user_input.rfind("yes")
#         last_occurrence_no = user_input.rfind("no")
#         last_occurrence = max(last_occurrence_yes, last_occurrence_no)
#         category_value = user_input[last_occurrence : last_occurrence + 3]
#     else:
#         speak("Can't understand. Please say 'yes' or 'no'.")
#         # user_input = None
#         return extract_binary_category()

#     return category_value


# def extract_city():
#     user_input = get_speech_input().lower()

#     nlp = spacy.load("en_core_web_sm")

#     doc = nlp(user_input)

#     cities = [ent.text for ent in doc.ents if ent.label_ == "GPE"]

#     if cities:
#         return cities[-1]
#     else:
#         return extract_city()


# def extract_job_title():
#     user_input = get_speech_input().lower()

#     job_titles = original_df["job_title"].unique()
#     for job_title in job_titles:
#         if job_title.lower() in user_input:
#             return job_title

#     speak("Can't understand. Please provide a valid job title.")
#     return extract_job_title()


# def extract_hereditary_diseases(user_hereditary_diseases):
#     user_hereditary_diseases_lower = user_hereditary_diseases.lower().strip()

#     if user_hereditary_diseases_lower == "yes":
#         speak("Could you specify which hereditary diseases are present in your family?")
#         command = get_speech_input()

#         diseases_list = original_df["hereditary_diseases"].unique()
#         user_diseases = []

#         for disease in diseases_list:
#             if disease.lower() in command:
#                 user_diseases.append(disease)

#         if not user_diseases:
#             speak("Can't understand. Please specify at least one hereditary disease.")
#             return extract_hereditary_diseases(user_hereditary_diseases)

#         return user_diseases

#     elif user_hereditary_diseases_lower == "no":
#         return ["NoDisease"]

#     else:
#         speak("Can't understand. Please say 'yes' or 'no'.")
#         return extract_hereditary_diseases(user_hereditary_diseases)


# def format_name(name):
#     format_word = "".join(word.capitalize() for word in name.split())
#     return format_word


# def extract_name():
#     input_text = get_speech_input()
#     matches_pattern = re.findall(r"my name is (\w+)", input_text, re.IGNORECASE)

#     if matches_pattern:
#         return matches_pattern[0]
#     else:
#         matches_words = re.findall(r"\b\w+\b", input_text)
#         valid_names = [
#             match
#             for match in matches_words
#             if match.lower() not in ["is", "my", "name"] and len(match) > 1
#         ]

#         if valid_names:
#             return valid_names[0]
#         else:
#             return None

# @app.route('/', methods=['Post'])
# def insurance_appFun():
    
#     speak("What is You name?")
#     user_name = extract_name()
#     user_name = 'thanos'
    

#     greet_user(user_name)

#     speak(
#         " Firstly, age, the age is a crucial factor in tailoring the best health insurance plan for you.Can you please tell me what is your age?"
#     )
#     user_age = extract_numeric_value()
    

#     speak(" Great, thank you. Now, could you share your current weight in pounds?")
#     user_weight = round(extract_numeric_value())
    

#     speak("Perfect. Next, can you tell me the city where you currently reside?")
#     user_city_name = extract_city()
#     user_city = format_name(user_city_name)
    

#     speak("Excellent. And what is your gender?")
#     user_gender = extract_gender()
    

#     speak("Thank you. Now, could you share a bit about your occupation or job?")
#     user_job = extract_job_title()
#     user_job_title = format_name(user_job)
    

#     speak(
#         "Great to know. Moving on, could you please share the number of family members you'd like to include in the plan?"
#     )
#     user_members = extract_numeric_value()

#     speak(
#         "Perfect. Now, are there any hereditary diseases or medical conditions that run in your family that we should be aware of?please say yes or no"
#     )
#     user_hereditary_diseases = extract_binary_category()
#     check_dieases = extract_hereditary_diseases(user_hereditary_diseases)

#     if user_hereditary_diseases == "yes" and check_dieases == "diabetes":
#         user_diabetes = "yes"
#     else:
#         user_diabetes = "no"
    

#     speak(
#         "Thank you for providing that information. Next, do you smoke?please say yes or no"
#     )
#     user_smoker = extract_binary_category()
    

#     speak("Now, could you please share your blood pressure levels in digits?")
#     user_bloodpressure = extract_numeric_value()
    

#     speak(
#         "Thank you for sharing that. Lastly, do you engage in regular exercise?please say yes or no"
#     )
#     user_regular_ex = extract_binary_category()
    

#     check_dieases_lower = [disease.lower() for disease in check_dieases]

#     matching_row = original_df[
#         (original_df["age"] == user_age)
#         & (original_df["sex"] == user_gender)
#         & (original_df["weight"] == user_weight)
#         & original_df["hereditary_diseases"].apply(
#             lambda x: any(disease in x.lower() for disease in check_dieases_lower)
#         )
#         & (original_df["members"] == user_members)
#         & (original_df["smoker"] == (1 if user_smoker == "yes" else 0))
#         & (original_df["city"] == user_city)
#         & (original_df["bloodpressure"] == user_bloodpressure)
#         & (original_df["diabetes"] == (1 if user_diabetes == "yes" else 0))
#         & (original_df["regular_ex"] == (1 if user_regular_ex == "yes" else 0))
#         & (original_df["job_title"] == user_job_title)
#     ]

#     if not matching_row.empty:
#         actual_charges = matching_row["claim"].min()
        
#         decimal_place = 2
#         rounded_charge = round(actual_charges, decimal_place)
#         speak(
#             f"So {user_name} Based on the information you provided, the estimated insurance charges for your tailored plan are: {rounded_charge}"
#         )
#         speak(
#             "Thank you for co-operate and sharing this informations. It will help us find the best health insurance plan for you."
#         )
#     else:
#         user_data = pd.DataFrame(
#             {
#                 "age": [user_age],
#                 "sex_male": [1 if user_gender == "male" else 0],
#                 "weight": [user_weight],
#                 "hereditary_diseases_NoDisease": [
#                     1 if user_hereditary_diseases == "yes" else 0
#                 ],
#                 "members": [user_members],
#                 "smoker": [1 if user_smoker == "yes" else 0],
#                 **{
#                     f"{col}_{user_input}": 1
#                     for col, user_input in zip(
#                         categorical_columns, [user_city, user_job_title]
#                     )
#                 },
#                 "bloodpressure": [user_bloodpressure],
#                 "diabetes": [1 if user_diabetes == "yes" else 0],
#                 "regular_ex": [1 if user_regular_ex == "yes" else 0],
#             },
#             columns=features.columns,
#         )

#         predicted_charge = reg.predict(user_data)

#         rounded_charge = round(predicted_charge[0])
        
#         new_entry = pd.DataFrame(
#             {
#                 "age": [user_age],
#                 "sex": [user_gender],
#                 "weight": [user_weight],
#                 "hereditary_diseases": [
#                     (
#                         "NoDisease"
#                         if user_hereditary_diseases == "no"
#                         else ", ".join(check_dieases)
#                     )
#                 ][0].replace('"', ""),
#                 "members": [user_members],
#                 "smoker": [1 if user_smoker == "yes" else 0],
#                 "city": [user_city],
#                 "bloodpressure": [user_bloodpressure],
#                 "diabetes": [1 if user_diabetes == "yes" else 0],
#                 "regular_ex": [1 if user_regular_ex == "yes" else 0],
#                 "job_title": [user_job_title],
#                 "claim": [rounded_charge],
#             },
#             columns=original_df.columns,
#         )
#         updated_df = pd.concat([original_df, new_entry], ignore_index=True)

#         updated_df.to_csv(file_path, index=False)

#         predicted_charge_rf = reg.predict(features)
#         mae_rf = mean_absolute_error(target, predicted_charge_rf)
#         r2_rf = r2_score(target, predicted_charge_rf)

#         print(f"Mean Absolute Error (Random Forest Regression): {mae_rf}")
#         print(f"R^2 Score (Random Forest Regression): {r2_rf}")
#         speak(
#             f" So {user_name} Based on the information you provided, the estimated insurance charges for your tailored plan are: {rounded_charge}"
#         )

#         speak(f"Thank you {user_name} for co-operate with us and sharing all informations. It will help us find the best health insurance plan for you.")
        
#         return f"So {user_name} Based on the information you provided, the estimated insurance charges for your tailored plan are: {rounded_charge} "    
    
# # if __name__ == "__main__":
# #     app.run(debug=True)

# from flask import Flask, request, jsonify, render_template
# import re
# import pandas as pd
# import pvorca


# app = Flask(__name__)

# orca = pvorca.create(access_key='89BlxJKCyiH/Eye4zhS74DxMibVpYlj/6qkLLw90NCm+ICw+AKYZqg==')


# def number_to_words(num):
#     # Define lists for ones, tens, and special cases up to 19
#     ones = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
#     teens = ['ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']
#     tens = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']

#     # Define the magnitude names
#     magnitudes = ['', 'thousand', 'million', 'billion', 'trillion', 'quadrillion', 'quintillion', 'sextillion', 'septillion', 'octillion', 'nonillion', 'decillion']

#     def convert_below_1000(n):
#         if n == 0:
#             return ''
#         elif n < 10:
#             return ones[n]
#         elif n < 20:
#             return teens[n - 10]
#         elif n < 100:
#             return tens[n // 10] + ' ' + convert_below_1000(n % 10)
#         else:
#             return ones[n // 100] + ' hundred ' + convert_below_1000(n % 100)

#     if num == 0:
#         return 'zero'

#     num_chunks = []
#     while num:
#         num_chunks.append(num % 1000)
#         num //= 1000

#     words_chunks = [convert_below_1000(chunk) + ' ' + magnitudes[i] for i, chunk in enumerate(num_chunks)]
#     words = ' '.join(words_chunks[::-1])  

#     return words.strip()
    
# def replace_numbers_with_words(input_text):
#     numeric_values = re.findall(r'\b\d+\b', input_text)
#     for num in numeric_values:
#         num_as_text = number_to_words(int(num))
#         input_text = input_text.replace(num, num_as_text)
#     return input_text


# def speak(response):
#     newText = replace_numbers_with_words(response)
    
#     orca.synthesize_to_file(newText,"output.wav")


# def extract_name(input_text):
#     matches_pattern = re.findall(r"my name is (\w+)", input_text, re.IGNORECASE)

#     if matches_pattern:
#         return matches_pattern[0]
#     else:
#         matches_words = re.findall(r"\b\w+\b", input_text)
#         valid_names = [
#             match
#             for match in matches_words
#             if match.lower() not in ["is", "my", "name"] and len(match) > 1
#         ]

#         if valid_names:
#             return valid_names[0]
#         else:
#             return None

# def extract_numeric_value(user_input):

#     numeric_values = []
#     numeric_str = ""
#     number_mapping = {
#         "zero": "0",
#         "one": "1",
#         "two": "2",
#         "three": "3",
#         "four": "4",
#         "five": "5",
#         "six": "6",
#         "seven": "7",
#         "eight": "8",
#         "nine": "9",
#         "ten": "10",
#     }

#     for word in user_input.lower().split():
#         if word.isdigit() or word.replace(".", "", 1).isdigit():
#             numeric_str += word
#         elif word in number_mapping:
#             numeric_str += number_mapping[word]
#         elif numeric_str:
#             numeric_values.append(numeric_str)
#             numeric_str = ""

#     if numeric_str:
#         numeric_values.append(numeric_str)

#     try:
#         last_sequence = numeric_values[-1]
#         numeric_value = (
#             float(last_sequence) if "." in last_sequence else int(last_sequence)
#         )
#         return numeric_value
#     except ValueError:
#         return extract_numeric_value()
#     except IndexError:
#         return extract_numeric_value()
    
# def extract_gender(user_input):
    

#     if "male" in user_input:
#         gender = "male"
#     elif "female" in user_input:
#         gender = "female"
#     else:
#         return extract_gender()

#     return gender

# def extract_job_title(user_input):
    
#     file_path = "insurance_data.csv"

#     original_df = pd.read_csv(file_path)

#     job_titles = original_df["job_title"].unique()
#     for job_title in job_titles:
#         if job_title.lower() in user_input:
#             return job_title

#     return extract_job_title()

# stored_responses = {}

# # Dictionary to map actions to response texts
# responses_dict = {
#     'ask_name': "What is your name?",
#     'ask_age': "How old are you?",
#     'ask_gender': "What is your gender?",
#     'ask_occupation': "What is your occupation?",
# }

# @app.route('/')
# def index():
#     return render_template("index.html")

# @app.route('/process_audio', methods=['POST'])
# def process_audio():
#     action = request.json.get('action', None)
    
#     # Get the response text from the dictionary
#     response_text = responses_dict.get(action, "Invalid action.")

#     return jsonify({'response_text': response_text})

# @app.route('/store_responses', methods=['POST'])
# def store_responses():
#     global stored_responses
#     responses = request.json
#     stored_responses = responses

#     name = extract_name(stored_responses['ask_name'])
#     age = extract_numeric_value(stored_responses['ask_age'])
#     gender = extract_gender(stored_responses['ask_gender'])
#     job_name = extract_job_title(stored_responses['ask_occupation'])
    
#     final_message = f"Alright, let's summarize: {name} is {age} years old, " \
#                 f"and identifies as {gender}. As for occupation, {name} is " \
#                 f"pursuing {job_name}. Quite an interesting combination!"
    
#     return jsonify({'final_message': final_message})

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, send_file
import pvorca

app = Flask(__name__)

orca = pvorca.create(access_key='89BlxJKCyiH/Eye4zhS74DxMibVpYlj/6qkLLw90NCm+ICw+AKYZqg==')

@app.route('/', methods=['GET'])
def get_audio():
    
    newText = "Hello My name is thanos and i am from Titan planet"   
    orca.synthesize_to_file(newText,"output.wav")
    
    return send_file("output.wav", as_attachment=False, mimetype='audio/wav')

if __name__ == '__main__':
    app.run(debug=True)
