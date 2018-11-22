import click
import requests
from halo import Halo
from bs4 import BeautifulSoup as Bs
import os

UPLOAD_ROUTE = "http://up.0se.ir/"
SHORTEN_ROUTE = "http://0se.ir/api/url.php?url="
ALLOWED_EXTENSIONS = ['zip', 'rar', 'png', 'jpg', 'gif']

@click.command()
@click.option('--file', '-f', help='File path to upload', type=click.File('rb'))
def cli(file):
    extension = os.path.splitext(file.name)[1][1:]
    if extension not in ALLOWED_EXTENSIONS:
        print("Sorry, Only %s are allowed. Try putting your file in an archive" % ALLOWED_EXTENSIONS)
        exit(-1)
    upload_spinner = Halo(text='Uploading', spinner='dots')
    upload_spinner.start()
    res = requests.post(UPLOAD_ROUTE, files={'upl': file})
    soap = Bs(res.text, "html.parser")
    link = soap.find("a")['href']
    if not link:
        upload_spinner.fail("Upload failed :(")
        exit(-1)
    upload_spinner.succeed("Uploaded successfully")
    shorten_link = requests.get(SHORTEN_ROUTE+link).text
    upload_spinner.succeed("Link has been shorten: http://%s" % shorten_link)


if __name__ == '__main__':
    cli()