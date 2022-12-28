import argparse
import os
import zipfile
from tqdm import tqdm
import requests

def zipdir(path, ziph):
    for root, dirs, files in tqdm(os.walk(path), total=len(list(os.walk(path)))):
        for file in files:
            if file[0] != '.':
                ziph.write(os.path.join(root, file))

        dirs[:] = [d for d in dirs if d[0] != '.']

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--directories', nargs='+', help='List of directories to include in the zip file')
    parser.add_argument('--files', nargs='+', help='List of files to include in the zip file')
    args = parser.parse_args()

    # Create the zip file
    with zipfile.ZipFile('partofleak.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add directories to the zip file
        for directory in args.directories:
            zipdir(directory, zipf)
        # Add files to the zip file
        for file in args.files:
            zipf.write(file)

    # Upload the zip file to AnonFiles
    files = {
        'file': ('partofleak.zip', open('partofleak.zip', 'rb')),
    }
    print("Here is the link for the zip file:")
    url = 'https://api.anonfiles.com/upload'
    response = requests.post(url, files=files)
    data = response.json()
    print(data['data']['file']['url']['short'])
