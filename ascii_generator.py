# ASCII art generator
# Gets an image from a URL and converts it to ASCII art
# Author: 22036

# Import the necessary modules
from PIL import Image
from io import BytesIO
import requests


# Define the function to get the user input URL
def get_image_url():
    url = input("Enter the URL of the image you want to convert: ")

    # Check if the URL starts with "http" or "https"
    if not url.startswith("http"):
        print(
            "Invalid URL, please include 'http://' or 'https://' in the beginning of the URL."
        )
        return get_image_url()

    return url


# Define the function to get the ASCII character set
def get_ascii_chars():
    # The default ASCII character set
    # blank to dark
    ascii_chars = [" ", ".", ",", ":", ";", "+", "*", "?", "%", "S", "#", "@"]

    # Ask the user if they want to customize the ASCII character set
    while True:
        print("Do you want to customize the ASCII character set? (y/n)")
        response = input().lower()
        if response == "y":
            ascii_chars = list(input("Enter the new set of ASCII characters: "))
            if len(ascii_chars) < 2:
                print("The ASCII character set must have at least 2 characters.")
                continue
            break
        elif response == "n":
            break
        else:
            print("Invalid response, please try again.")

    # Ask the user if they want to reverse the ASCII character set
    while True:
        print("Do you want to reverse the ASCII character set? (y/n)")
        response = input().lower()
        if response == "y":
            ascii_chars = ascii_chars[::-1]
            break
        elif response == "n":
            break
        else:
            print("Invalid response, please try again.")

    return ascii_chars


# Define the function to convert the image to ASCII
def convert_to_ascii(img, ascii_chars):
    ascii_img = ""
    pixels = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            brightness = int((r + g + b) / 3)
            char_index = int(brightness / (255 / len(ascii_chars)))
            if char_index == len(ascii_chars):
                char_index -= 1
            ascii_img += ascii_chars[char_index]
        ascii_img += "\n"

    return ascii_img


# Define the function to apply a color filter to the image
def apply_color_filter(img, color):
    r, g, b = img.split()

    if color == "red":
        img = Image.merge(
            "RGB", (r, Image.new("L", img.size, 0), Image.new("L", img.size, 0))
        )

    elif color == "green":
        img = Image.merge(
            "RGB", (Image.new("L", img.size, 0), g, Image.new("L", img.size, 0))
        )

    elif color == "blue":
        img = Image.merge(
            "RGB", (Image.new("L", img.size, 0), Image.new("L", img.size, 0), b)
        )

    width, height = img.size
    img = img.resize((int(width), int(height * 2)))

    return img


def main():
    # Get the user input URL and load the image
    url = get_image_url()
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
    except:
        print("Invalid URL, please try again.")
        exit()

    # Load the image and downscale it for better ASCII conversion
    # Since the ASCII characters are taller than they are wide,
    # we need to downscale the image by a factor of [scale] in width and [scale]*2 in height
    width, height = img.size
    # ask the user for the downscale factor
    print("Enter the downscale factor (1 ~ 10, 5 for default.): ")
    try:
        scale = int(input())
        if scale < 1 or scale > 10:
            print("Invalid downscale factor, using the default value (5).")
            scale = 5
    except:
        print("Invalid downscale factor, using the default value (5).")
        scale = 5
    img = img.resize((int(width / scale), int(height / (scale * 2))))

    # Get the ASCII character set and convert the image to ASCII
    ascii_chars = get_ascii_chars()
    ascii_img = convert_to_ascii(img, ascii_chars)

    # Print the ASCII image
    print(ascii_img)

    # Apply a color filter to the image
    print("Do you want to apply a color filter to the image? (y/n)")
    response = input().lower()
    if response == "y":
        print("Which color filter do you want to apply? (red/green/blue)")
        color = input().lower()
        img = apply_color_filter(img, color)
        img.show()

    # Save the ASCII art to a text file
    # filename should not include the file extension
    # the file extension(.txt) will be added automatically
    filename = input("Enter the filename to save the ASCII art: ")
    with open("outputs/" + filename + ".txt", "w") as file:
        file.write(ascii_img)

    print(f"The ASCII art has been saved to {filename}.")


if __name__ == "__main__":
    main()

# EOF
