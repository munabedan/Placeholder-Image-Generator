import argparse
from PIL import Image, ImageDraw, ImageFont


def generate_grey_placeholder_image(dimensions, color, no_border, no_size):
    width, height = map(int, dimensions.split('x'))
    image = Image.new('RGB', (width, height), color)

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Draw black border if not disabled
    if not no_border:
        border_width = 2
        draw.rectangle([(border_width, border_width), (width - border_width - 1, height - border_width - 1)], outline="black")

    # Draw diagonal line within the border if not disabled
    if not no_border and not no_size:
        draw.line([(2, height - 2), (width - 2, 2)], fill="black", width=1)

    # Draw text indicating the dimensions in the middle if not disabled
    if not no_size:
        text = f"{width}px x {height}px"
        font = ImageFont.load_default()  # You can adjust the font here

        # Calculate text size
        text_width = draw.textlength(text, font=font)
        text_height = 36

        # Calculate text position
        text_position = ((width - text_width) // 2, (height - text_height) // 2)

        # Draw rectangle to hide section of the line covered by the text
        draw.rectangle([text_position, (text_position[0] + text_width, text_position[1] + text_height)], fill=color)

        # Draw text
        draw.text(text_position, text, fill="black", font=font)

    return image


def save_image(image, filename):
    image.save(filename)


def main():
    parser = argparse.ArgumentParser(description='Generate grey placeholder images')
    parser.add_argument('-d', '--dimensions', type=str, required=True,
                        help='Dimensions of the image in the format WIDTHxHEIGHT')
    parser.add_argument('-c', '--color', type=str, default='#8f96a3',
                        help='Color of the image in hexadecimal format')
    parser.add_argument('-f', '--format', type=str, default='png',
                        help='Format of the image (e.g., png, jpg)')
    parser.add_argument('-n', '--name', type=str, default='placeholder',
                        help='Name of the output image file')
    parser.add_argument('--no-border', action='store_true', help='Disable border')
    parser.add_argument('--no-size', action='store_true', help='Disable text and diagonal line')
    args = parser.parse_args()

    image = generate_grey_placeholder_image(args.dimensions, args.color, args.no_border, args.no_size)
    save_image(image, f"{args.name}.{args.format}")


if __name__ == "__main__":
    main()
