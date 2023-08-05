import openai


def init_openai(secret_key: str)-> None:
    """Initialize OpenAI by giving Secret Key

    Args:
        secret_key (str): OpenAI Secret Key
    """
    openai.api_key = secret_key


def show_model()-> None:
    """AI is creating summary for show_model

    """
    openai.Model.list()


def create_images(prompt: str, img_size: str, num_images: int) -> list:
    """Create Image from a Prompt using the OpenAI DALL-E model.

    Args:
        prompt (str): Message prompt to be used to generate the image.
        img_size (str): Image pixel size. Accepts the following inputs:
                        ["256x256", "512x512", "1024x1024"]
        num_images (int): Number of images to request.

    Returns:
        list: List of URL of all the Generated Images.
    """
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=num_images,
            size=img_size
        )
    except openai.error.OpenAIError as e:
        print(e.http_status)
        print(e.error)
        return []

    image_urls = list()
    for data in response.get('data', []):
        image_urls.append(data['url'])

    return image_urls
