from io import BytesIO
from PIL import Image
import click
import json
import os
import requests
import tqdm

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'


def unpuzzle_image(input_image):
    size = input_image.size

    # use the original image for the right and bottom edges
    output_image = input_image.copy()

    div = 4
    mult = 8
    col_width = (size[0] // (div * mult)) * mult
    row_height = (size[1] // (div * mult)) * mult

    # transpose grids
    for col in range(4):
        for row in range(4):
            box = (
                col * col_width,
                row * row_height,
                (col + 1) * col_width,
                (row + 1) * row_height
            )
            region = input_image.crop(box)
            output_image.paste(region, (row * col_width, col * row_height))

    return output_image


@click.group()
def cli():
    pass


@cli.command()
@click.argument('episode_uri')
@click.option('--email', required=True)
@click.option('--password', required=True)
def download(episode_uri, email, password):
    login_uri = 'https://shonenjumpplus.com/user_account/login'
    data = {
        'email_address': email,
        'password': password,
        'return_location_path': '/'
    }
    headers = {
        'user-agent': USER_AGENT,
        'x-requested-with': 'XMLHttpRequest'
    }
    with requests.session() as session:
        # login
        response = session.post(login_uri, headers=headers, data=data)

        # get json
        json_uri = f'{episode_uri}.json'
        response = session.get(json_uri, headers=headers)
        json_data = json.loads(response.text)

        # create directory
        dirname = json_data['readableProduct']['title']
        if not os.path.exists(dirname):
            os.mkdir(dirname)

        # download images
        pages = json_data['readableProduct']['pageStructure']['pages']
        for index, page in enumerate(tqdm.tqdm(pages, total=len(pages))):
            if 'src' in page:
                image_uri = page['src']
                response = session.get(image_uri)

                image_bytes = response.content
                puzzled_image = Image.open(BytesIO(image_bytes))
                unpuzzled_image = unpuzzle_image(puzzled_image)
                box = (0, 0, width, height)

                filename = f'{str(index).zfill(4)}.jpg'
                path = os.path.join(dirname, filename)
                unpuzzled_image.save(path)


def main():
    cli()


if __name__ == '__main__':
    main()
