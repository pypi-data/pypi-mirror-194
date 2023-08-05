# Wrapper for OpenAI DALL-E Image Generator
Wrapper for Image Generation using DALL-E from OpenAI.

## Prerequisites
1. `Python 3.7+`
2. `pip`
3. Account at [OpenAI](https://beta.openai.com/). Make sure you have a Secret Key.

## Install the code.
1. Install `poetry`
```
python3 -m pip install poetry
```
2. Download the codebase and open the folder.
```
git clone
cd ai_img_gen
```
3. Install the necessary packages and environment via `poetry`.
```
poetry install
```
4. Create a `.env` file by copying the sample.env and filling it up the details.
```
cp sample.env .env
nano .env
```

## Run the code.
```
poetry run python run.py
```
