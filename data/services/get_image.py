from aiogram.types import URLInputFile


def get_avatar(url):
    if not url:
        url = 'https://petrovka-38.com/images/petrovka/2017/1/9/115344820161227.jpg'
    avatar = URLInputFile(url)
    return avatar
