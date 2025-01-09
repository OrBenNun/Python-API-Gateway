import json
import requests
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

def read_validation_rules(file_path):
    with open(file_path, 'r') as file:
        validation_rules = json.load(file)
    return validation_rules


def send_to_gemini(validation_rules):
    # # Replace with the actual endpoint and API key for Gemini LLM
    # url = "https://api.gemini.com/v1/generate_code"
    # headers = {
    #     "Content-Type": "application/json",
    #     "Authorization": f"Bearer {os.getenv('GEMINI_API_KEY')}"
    # }
    # payload = {
        # "prompt": "Generate Python code to validate the following rules:",
        # "rules": validation_rules
    # }
    # response = requests.post(url, headers=headers, json=payload)
    # return response.json()['generated_code']
    
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel(
                            model_name='gemini-1.5-pro',
                            tools='code_execution')
    
    # response = model.generate_content((
    # 'prompt: "Generate Python code to validate the parameters of the following api config file with the following rules:',
    # f"rules: {validation_rules}",
    # "Dont write any docs, write only the python code."))
    response = model.generate_content((
    '''
        Generate Python code to validate API request parameters based on the following API configuration JSON. 
        The script should:
        - Understand the structure of the API configuration JSON.
        - Create rules to validate the parameters of each endpoint.
        - Validate the parameters based on the rules.
        - Raise an error if a parameter does not meet the validation rules.
        - Include appropriate error messages for each validation rule.
        - Handle missing parameters and incorrect data types.
        - Handle unkwon parameters and raise an error if an unknown parameter is present.
        - The validation function should get the raw data from the request for example: {
        "username": "testuser",
        "password": "password123"
        }
        - Write only the Python code, and ensure the output does not include any comments, example usage, or additional text. 

        Here is the configuration:
        ''',
        f"{validation_rules}"))
    # '''
    # Generate Python code to validate the parameters of the following API config file with the specified rules. 
    # Write only the Python code, and ensure the output does not include any comments, example usage, or additional text. 
    # Respond with just the code and nothing else.
    # ''',
    # f"rules: {validation_rules}"))

    return response.text

def save_generated_code(code, output_file):
    with open(output_file, 'w') as file:
        file.write(code)
        
def clean_code_output(raw_output):
    lines = raw_output.splitlines()
    filtered_lines = [line for line in lines if not line.strip().startswith("```")]
    return "\n".join(filtered_lines)

def clean_file(filepath: str):
    try:
        # Read the content of the file
        with open(filepath, 'r', encoding='utf-8') as file:
            raw_content = file.read()

        # Clean the content
        cleaned_content = clean_code_output(raw_content)

        # Save the cleaned content back to the file
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(cleaned_content)

        print(f"File '{filepath}' cleaned and saved successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     file_path = 'config/validation_rules.json'
#     validation_rules = read_validation_rules(file_path)
#     generated_code = send_to_gemini(validation_rules)
#     save_generated_code(generated_code, 'llm_validation.py')
#     clean_file('llm_validation.py')

def ai_validation_func():
    file_path = 'config/validation_rules.json'
    validation_rules = read_validation_rules(file_path)
    generated_code = send_to_gemini(validation_rules)
    save_generated_code(generated_code, 'llm_validation.py')
    clean_file('llm_validation.py')
    
if __name__ == "__main__":
    ai_validation_func()