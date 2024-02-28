import streamlit as st
import pandas as pd
import replicate
import base64
import requests

# UI configurations
st.set_page_config(page_title="Replicate Image Generator based on CSV Input", page_icon="🌟")

# API Tokens and endpoints from `.streamlit/secrets.toml` file
REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]
REPLICATE_MODEL_ENDPOINTSTABILITY = st.secrets["REPLICATE_MODEL_ENDPOINTSTABILITY"]
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]  # Add your GitHub token to your Streamlit secrets
GITHUB_REPOSITORY = "mannurkishorreddy/streamlit-replicate-img-app"  # Replace with your GitHub repository

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
    df = pd.read_csv("prompts.csv")  # Replace with your CSV file path
    options = df['Prompts'].tolist()  # Replace with your column name
    st.sidebar.title("Choose Your Prompt")
    selected_prompt = st.sidebar.selectbox('', options, index=0, help="Select a prompt from the list")

    # Main area
    st.title(" Replicate AI Image Generator")
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
                    image_url = output[0]  # Assuming the output is a list of image URLs
                    st.image(image_url, caption="Generated Image", use_column_width=True)
                    # Add a button to save the image to GitHub
                    if st.button("Save the Image", key='save'):
                        # Convert image URL to base64-encoded content
                        response = requests.get(image_url)
                        image_content = base64.b64encode(response.content).decode('utf-8')
                        # Set filename and commit message
                        filename = "generated_image.png"  # You can make this more unique if needed
                        commit_message = "Add generated image"
                        # Call the function to save the image to GitHub
                        save_image_to_github(
                            image_content, 
                            filename, 
                            GITHUB_REPOSITORY, 
                            "/images",  # Replace with the path to your folder in the repository
                            commit_message, 
                            GITHUB_TOKEN
                        )
            except Exception as e:
                st.error(f'Encountered an error: {e}')

if __name__ == "__main__":
    main()
