import json
import google.generativeai as genai
# import example.memegen as memegen
import random


# Step 1: Load the templates.json
def load_templates(json_file):
    with open(json_file, 'r') as file:
        templates = json.load(file)
    return templates

# Step 2: Extract keywords using Gemini from user description
def extract_keywords_from_description(description):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Extract keywords from this description that best describe emotions and reactions needed for a meme (max 10 keywords. one keywords for each line only. return keywords only. no description. no explanation. no numbering.): {description}"
    result = model.generate_content([prompt])
    keywords = result.text.splitlines()  # Assuming keywords are split by lines
    return keywords

# Step 3: Find the best matching template based on keywords
def select_random_template(templates):
    return random.choice(templates)

def find_best_template(templates, keywords):
    best_template = None
    max_matching_keywords = 0

    for template in templates:
        template_keywords = template['keywords']
        # Count matching keywords
        matching_keywords = len(set(template_keywords) & set(keywords))
        if matching_keywords > max_matching_keywords:
            best_template = template
            max_matching_keywords = matching_keywords

    return best_template

# Step 4: Generate meme text using the selected template keywords and number of text lines
def generate_meme_text(template, description, num_lines):
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Send template keywords and number of lines needed to Gemini to suggest meme text
    prompt = f"Generate {num_lines} lines of meme text based on these keywords: {', '.join(template['keywords'])}. And for this description: {description}. return only the text lines. no explanation. no numbering."
    result = model.generate_content([prompt])

    meme_text_lines = result.text.splitlines()[:num_lines]  # Ensure we get the required number of lines
    return meme_text_lines

# Step 5: Main function that orchestrates the entire process
async def generate_meme_from_description(description, json_file):
    # Load templates
    templates = load_templates(json_file)

    # Extract keywords from the user's description
    prompt_keywords = extract_keywords_from_description(description)
    print(f"Extracted keywords: {prompt_keywords}")

    # Find the best matching template based on the extracted keywords
    # best_template = find_best_template(templates, prompt_keywords)
    best_template = select_random_template(templates)
    if best_template is None:
        print("No matching template found.")
        return

    print(f"Selected template: {best_template['name']}")

    # Get the number of text lines supported by the template
    num_lines = best_template['lines']

    # Generate meme text based on template keywords and number of lines
    meme_text = generate_meme_text(best_template, description, num_lines)

    lines=[]
    print("Generated meme text:")
    for line in meme_text:
        print(line)
        lines.append(line)

    return best_template['id'], lines

# Example usage:
# description = "a meme about programmer and his problem with semicolon"
# json_file = "templates.json"
# template_name, texts = generate_meme_from_description(description, json_file)
# meme_url = memegen.generate_meme(template_name, texts, 'meme.jpg')

