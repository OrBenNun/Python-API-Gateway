# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch
# import json


# # model_name = "Salesforce/codet5-small" 
# # model = AutoModelForCausalLM.from_pretrained(model_name)
# # tokenizer = AutoTokenizer.from_pretrained(model_name)

# from transformers import RobertaTokenizer, T5ForConditionalGeneration
# tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-small')
# model = T5ForConditionalGeneration.from_pretrained('Salesforce/codet5-small')

# # Function to load validation rules from a JSON file
# def load_validation_rules_from_file(file_path='config\validation_rules.json'):
#     # config\validation_rules.json
#     with open(file_path, 'r') as f:
#         return json.load(f)

# # Function to communicate with the CodeParrot model to generate validation code
# def generate_validation_code(validation_rules):
#     prompt = f"""
#     Based on the following validation rules, generate Python code to validate HTTP request parameters.

#     {json.dumps(validation_rules, indent=2)}

#     The generated code should:
#     1. Check if required parameters are present.
#     2. Check if the parameter types are correct.
#     3. Check if parameters meet the specified constraints (min/max length, min/max value, etc.).
#     4. Raise a meanfull Execption for any invalid parameters.
#     """
    
#     inputs = tokenizer(prompt, return_tensors="pt")
    
#     # Generate code
#     outputs = model.generate(inputs['input_ids'], max_length=1000)
#     generated_code = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
#     return generated_code

# # Function to save the generated validation code to a Python file
# def save_validation_code_to_file(validation_code, file_path='llm_parameter_validation.py'):
#     with open(file_path, 'w') as f:
#         f.write(validation_code)

# # def ai_validate_parameters():

# # Example Usage
# validation_rules = load_validation_rules_from_file()
# validation_code = generate_validation_code(validation_rules)

# # Save the generated validation code to a Python file
# save_validation_code_to_file(validation_code)

# # The generated code will be saved to 'llm_parameter_validation.py'


import os
import json
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import RobertaTokenizer, T5ForConditionalGeneration

class AIValidator:
    def __init__(self, model_name="codet5-small", validation_file="config/validation_rules.json"):
        self.model_name = model_name
        # self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        # self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-small')
        self.model = T5ForConditionalGeneration.from_pretrained('Salesforce/codet5-small')
        self.validation_file = validation_file

    def get_validation_file_path(self):
        # Dynamically locate the validation file relative to the project's root directory
        project_root = os.path.abspath(os.path.dirname(__file__))  # Locate current file's directory
        file_path = os.path.join(project_root, "..", self.validation_file)  # Adjust for config directory
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Validation file not found at {file_path}")
        return file_path

    def load_validation_rules(self):
        # Load validation rules from JSON
        file_path = self.get_validation_file_path()
        with open(file_path, 'r') as f:
            return json.load(f)

    def generate_validation_code(self, validation_rules):
        # Create a prompt and generate Python code
        prompt = f"""
        Based on the following validation rules, generate Python code to validate HTTP request parameters.

        {json.dumps(validation_rules, indent=2)}

        The generated code should:
        1. Check if required parameters are present.
        2. Check if the parameter types are correct.
        3. Check if parameters meet the specified constraints (min/max length, min/max value, etc.).
        4. Raise a BadRequest exception for any invalid parameters.
        """
        
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(inputs['input_ids'], max_length=1000)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def save_validation_code(self, validation_code, file_path="llm_parameter_validation.py"):
        # Save the generated validation code to a file
        with open(file_path, 'w') as f:
            f.write(validation_code)

# Example usage
if __name__ == "__main__":
    ai_validator = AIValidator()
    try:
        rules = ai_validator.load_validation_rules()
        code = ai_validator.generate_validation_code(rules)
        ai_validator.save_validation_code(code)
        print("Validation code successfully generated and saved to llm_parameter_validation.py")
    except Exception as e:
        print(f"Error: {e}")


