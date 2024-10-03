import requests

def replace_with_tilde_keys(text):
    # Define the replacements in a dictionary (reverse mapping)
    replacements = {
        "?": "~q", "&": "~a", "%": "~p", "#": "~h", "/": "~s",
        "\\": "~b", "<": "~l", ">": "~g", '"': "''"
    }
    
    # Replace special characters with their tilde-based equivalents
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    
    # Replace whitespace with underscores
    text = text.replace(" ", "_")
    
    return text

def generate_meme(template, text_list, save_path):
    """
    Generates a meme using the Memegen API and saves it locally.

    Args:
        template (str): Template name (e.g., 'ds').
        text_list (list): List of strings for the meme text (up to 2 or more lines).
        save_path (str): Path where the image will be saved locally.
    
    Returns:
        str: The URL of the generated meme.
    """
    # Create the URL for the meme using the Memegen API
    base_url = "https://api.memegen.link/images"
    
    # Join the text in the list, replacing spaces with underscores for URL encoding
    text_list = [replace_with_tilde_keys(text) for text in text_list]
    
    # Build the full URL
    meme_url = f"{base_url}/{template}/{'/'.join(text_list)}.jpg"

    # Request the meme image
    response = requests.get(meme_url)
    
    if response.status_code == 200:
        # Save the image locally
        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"Meme saved successfully at {save_path}")
    else:
        print(f"Failed to generate meme. Status code: {response.status_code}")
    
    return meme_url

# Example usage
# template_name = "ds"  # Template name (e.g., 'ds' for Drake meme)
# texts = ["high quality", "small file"]  # List of text for the meme
# save_file_path = "meme.jpg"  # Path where the image will be saved

# meme_url = generate_meme(template_name, texts, save_file_path)
# print(f"Meme URL: {meme_url}")
