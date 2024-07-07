import sys
import os

def main():
    if len(sys.argv) != 4:
        print("Usage: python process_file.py <file_path> <id> <input_string>")
        sys.exit(1)
    
    file_path, file_id, input_string = sys.argv[1], sys.argv[2], sys.argv[3]
    
    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)
    
    # Read the content of the input file
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Prepare the new content
    new_content = f"{content}\nInput text: {input_string}\nLength of input text: {len(input_string)}"
    
    # Get the directory and base name of the file
    directory, base_name = os.path.split(file_path)
    file_name, file_extension = os.path.splitext(base_name)
    
    # Prepare the output file path
    output_file_path = os.path.join(directory, f"{file_name}.Output")
    
    # Write the new content to the output file
    with open(output_file_path, 'w') as output_file:
        output_file.write(new_content)
    
    print(f"Processed file saved as '{output_file_path}'")

if __name__ == "__main__":
    main()
