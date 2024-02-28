import streamlit as st
import pandas as pd
import replicate
import base64
import requests
import io
from PIL import Image

# UI configurations
st.set_page_config(page_title="Replicate Image Generator based on CSV Input", page_icon="🌟")

# API Tokens and endpoints from `.streamlit/secrets.toml` file
REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]
REPLICATE_MODEL_ENDPOINTSTABILITY = st.secrets["REPLICATE_MODEL_ENDPOINTSTABILITY"]
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
GITHUB_REPOSITORY = "mannurkishorreddy/streamlit-replicate-img-app"

# Function to convert the image to JPEG
def convert_to_jpeg(image_content):
    """
    Convert image content to JPEG format.
    """
    image = Image.open(io.BytesIO(image_content))
    with io.BytesIO() as output_stream:
        image.save(output_stream, format="JPEG")
        return output_stream.getvalue()

# Function to save the image to GitHub
def save_image_to_github(image_content, filename, repo_name, path_in_repo, commit_message, github_token):
    """
    Saves an image to GitHub repository.
    Args are similar to the earlier provided function.
    """
    url = f"https://api.github.com/repos/{repo_name}/contents/{path_in_repo}/{filename}"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {
        "message": commit_message,
        "content": image_content,
        "branch": "main",
    }
    response = requests.put(url, json=data, headers=headers)
    if response.status_code == 201:
        st.success("Image successfully uploaded to GitHub.")
    else:
        st.error(f"Failed to upload image: {response.content}")

def main():
    # Sidebar with CSV prompt selection
    df = pd.read_csv("prompts.csv")
    options = df['Prompts'].tolist()
    st.sidebar.title("Choose Your Prompt")
    selected_prompt = st.sidebar.selectbox('', options, index=0, help="Select a prompt from the list")

    # Main area
    st.title("Replicate AI Image Generator")
    st.markdown("### Transform your ideas into stunning visuals!")
    
    if st.button('Generate Image', key='generate'):
        with st.spinner('🧚‍♂️ Creating magic...'):
            try:
                # Call to the replicate API to get the image
                output = replicate.run(
                    REPLICATE_MODEL_ENDPOINTSTABILITY,
                    input={
                        "prompt": selected_prompt,
                        "width": 1024,
                        "height": 1024,
                        "num_outputs": 1
                    }
                )
                if output:
                    # Save the image URL in the session state
                    st.session_state['generated_image_url'] = output[0]
                    st.image(st.session_state['generated_image_url'], caption="Generated Image", use_column_width=True)
            except Exception as e:
                st.error(f'Encountered an error: {e}')
    
    # Save button and functionality
    if 'generated_image_url' in st.session_state:
        # Re-display the image
        st.image(st.session_state['generated_image_url'], caption="Generated Image", use_column_width=True)
        
        if st.button("Save the Image", key='save'):
            # Fetch the image content from the URL
            response = requests.get(st.session_state['generated_image_url'])
            if response.status_code == 200:
                # Convert the image to JPEG
                jpeg_content = convert_to_jpeg(response.content)
                # Encode to base64
                image_content_base64 = base64.b64encode(jpeg_content).decode('utf-8')
                # Set filename and commit message
                filename = f"{selected_prompt.replace(' ', '_')}.jpeg"
                commit_message = "Add generated image"

                # Save the image to GitHub
                save_image_to_github(
                    image_content_base64, 
                    filename, 
                    GITHUB_REPOSITORY, 
                    "images",  # Assuming there is a folder named 'images' in your repository
                    commit_message, 
                    GITHUB_TOKEN
                )
            else:
                st.error(f"Failed to fetch the generated image for saving. Status code: {response.status_code}")

if __name__ == "__main__":
    main()
