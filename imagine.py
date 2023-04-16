# <A>: Dennis Vink
# <@>: dennis@drvink.com
# <W>: https://drvink.com
# <L>: https://linkedin.com/in/drvink/

import argparse
import json
import openai
import os

from base64 import b64decode
from pathlib import Path

def main(prompt, path, dimension):
    DATA_DIR = Path(path)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size=dimension,
        response_format="b64_json",
    )

    image_data = response['data'][0]['b64_json']
    decoded_image_data = b64decode(image_data)

    file_name = DATA_DIR / f"{prompt[:5].lower().replace(' ', '_')}-{response['created']}.png"

    with open(file_name, mode="wb") as file:
        file.write(decoded_image_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate image from OpenAI API.')
    parser.add_argument('-pr', '--prompt', type=str, help='The prompt for the OpenAI API')
    parser.add_argument('-o', '--output', type=str, help='Path to save the images, defaults to current directory')
    parser.add_argument('-d', '--dimension', type=str, help='Dimension, defaults to 1024x1024.')

    args = parser.parse_args()

    if args.dimension:
        dimension = args.dimension
    else:
        dimension = "1024x1024"
    if args.output:
        path = args.output
    else:
        path = './'
    if args.prompt:
        prompt = args.prompt
    else:
        prompt = input("Please enter a prompt: ")

    main(prompt, path, dimension)
