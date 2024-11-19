import os
import subprocess

# Define the directories
image_dir = 'samples/images'
text_dir = 'samples/texts'
output_dir = 'outputs'

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to process files
def process_file(input_file, output_compressed, output_decompressed):
    # Construct the log file path
    log_file_path = os.path.basename(input_file)
    log_file_path = f"{output_dir}/{os.path.splitext(log_file_path)[0]}.log"
    
    # Open the log file in write mode and redirect stdout and stderr to it
    with open(log_file_path, 'w') as log_file:
        subprocess.run(
            ['python3', 'Main_Fixo.py', input_file, output_compressed, output_decompressed],
            stdout=log_file,
            stderr=log_file
        )

# Process text files
for text_file in os.listdir(text_dir):
    text_path = os.path.join(text_dir, text_file)
    if os.path.isfile(text_path):  # Ensure it's a file, not a directory
        output_compressed = os.path.join(output_dir, f"{text_file}_compressed")
        output_decompressed = os.path.join(output_dir, f"{text_file}_decompressed")
        process_file(text_path, output_compressed, output_decompressed)

# Process image files
for image_file in os.listdir(image_dir):
    image_path = os.path.join(image_dir, image_file)
    if os.path.isfile(image_path):  # Ensure it's a file, not a directory
        output_compressed = os.path.join(output_dir, f"{image_file}_compressed")
        output_decompressed = os.path.join(output_dir, f"{image_file}_decompressed")
        process_file(image_path, output_compressed, output_decompressed)
