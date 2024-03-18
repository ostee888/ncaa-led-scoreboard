from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

def add_text_to_image(image, text, position, font_size, font_index):
    """
    Add text to the given image at the specified position with the specified font size.

    Args:
        image (Image): The image to which text will be added.
        text (str): The text to be added.
        position (tuple): The (x, y) position where the middle of the text will be drawn.
        font_size (int): The font size of the text.
        font_index (int): The index of the font to be used.
    """
    try:
        draw = ImageDraw.Draw(image)
        # Define fonts with their paths
        fonts = [
            "/usr/share/fonts/truetype/5x5-sans.ttf",  #1
            "/usr/share/fonts/truetype/CGpixel3x5.ttf",  #2
            "/usr/share/fonts/truetype/EightBitDragon-anqx.ttf", #3
            "/usr/share/fonts/truetype/6x6-pixel-yc-fs.ttf", #4
            "/usr/share/fonts/truetype/press-play.ttf", #5
            "/usr/share/fonts/truetype/8x-pixelated.ttf"  #6          
        ]
        font_path = fonts[min(font_index, len(fonts) - 1)]  # Choose the font based on font_index
        
        font = ImageFont.truetype(font_path, font_size)
        
        # Get the width and height of the text
        text_width, text_height = draw.textsize(text, font=font)
        
        # Calculate the adjusted position to place the middle of the text
        adjusted_position = (position[0] - text_width // 2, position[1] - text_height // 2)
        
        draw.text(adjusted_position, text, fill="white", font=font)
    except Exception as e:
        print("Error:", e)

def add_logo_to_image(image, logo_url, position, target_height):
    """
    Add a logo to the given image at the specified position and resize it to the target height.

    Args:
        image (Image): The image to which the logo will be added.
        logo_url (str): The URL of the logo image file.
        position (tuple): The (x, y) position where the middle of the logo will be pasted.
        target_height (int): The target height of the logo after resizing.
    """
    try:
        response = requests.get(logo_url)
        logo_image = Image.open(BytesIO(response.content))
        logo_image = logo_image.resize((target_height, target_height))
        
        # Get the width and height of the logo
        logo_width, logo_height = logo_image.size
        
        # Calculate the adjusted position to place the middle of the logo
        adjusted_position = (position[0] - logo_width // 2, position[1] - logo_height // 2)
        
        image.paste(logo_image, adjusted_position)
    except Exception as e:
        print("Error:", e)

def compose_image(texts, text_positions, text_font_sizes, logo_urls, logo_positions, logo_target_heights, matrix_width, matrix_height):

    """
    Compose an image with text and logos, and return it.

    Args:
        texts (list): List of texts to display.
        text_positions (list): List of (x, y) positions for each text.
        text_font_sizes (list): List of font sizes for each text.
        logo_urls (list): List of URLs of the logo image files.
        logo_positions (list): List of (x, y) positions for each logo.
        logo_target_heights (list): List of target heights for each logo.
        matrix_width (int): Width of the matrix.
        matrix_height (int): Height of the matrix.

    Returns:
        Image: The composed image.
    """
    try:
        composed_image = Image.new("RGB", (matrix_width, matrix_height), color="black")
        
        # Add text elements to the composed image
        for text, position, font_size in zip(texts, text_positions, text_font_sizes):
            add_text_to_image(composed_image, text, position, font_size)
        
        # Add logo elements to the composed image
        for logo_url, position, target_height in zip(logo_urls, logo_positions, logo_target_heights):
            add_logo_to_image(composed_image, logo_url, position, target_height)

        return composed_image

    except Exception as e:
        print("Error:", e)

def create_blank_image(width, height):
    """
    Create a blank image with the specified width and height.

    Args:
        width (int): The width of the image.
        height (int): The height of the image.

    Returns:
        Image: A blank image.
    """
    return Image.new("RGB", (width, height), color="black")