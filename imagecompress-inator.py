import os
import base64
from PIL import Image
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

def process_image(file_path):
    """Process a single image: resize and encode to base64."""
    try:
        with Image.open(file_path) as img:
            # Resize image to a maximum of 10x10 pixels while maintaining aspect ratio
            img.thumbnail((10, 10), Image.LANCZOS)

            # Save the image to a BytesIO object
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            return os.path.basename(file_path), base64.b64encode(buffered.getvalue()).decode('utf-8')
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return os.path.basename(file_path), None

def encode_images_to_base64(folder_path, output_folder, new_images_only):
    """Encode all JPEG images in a folder to base64 format and save them in an output folder."""
    base64_images = {}

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Use ThreadPoolExecutor to process images in parallel for better performance
    with ThreadPoolExecutor() as executor:
        # Gather all image paths
        image_paths = [
            os.path.join(folder_path, filename)
            for filename in os.listdir(folder_path)
            if filename.lower().endswith(('.jpeg', '.jpg'))
        ]
        
        # Process each image
        for image_path in image_paths:
            filename = os.path.basename(image_path)
            output_file_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.datauri")  # Change to .datauri
            
            # Check if the output file already exists and skip processing if required
            if new_images_only and os.path.exists(output_file_path):
                print(f"Skipping already processed image: {filename}")
                continue

            # Map the process_image function to the current image path
            result = process_image(image_path)
            if result and result[1] is not None:  # Check if the base64 string is not None
                base64_images[result[0]] = result[1]
                # Format as data URI
                data_uri = f"data:image/jpeg;base64,{result[1]}"
                # Save data URI to a file
                with open(output_file_path, 'w') as output_file:
                    output_file.write(data_uri)
            else:
                print(f"Skipping saving for {filename} due to processing error.")

    return base64_images

# Specify the path to the folder containing the JPEG images and the output folder
input_folder_path = 'fullres/'  # Folder with .jpeg images
output_folder_path = 'base64/'    # Folder to save base64-encoded images
new_images_only = True  # Set to True to skip existing images

base64_encoded_images = encode_images_to_base64(input_folder_path, output_folder_path, new_images_only)

# Print a confirmation message
print(f"Base64 encoded images saved in: {output_folder_path}")
