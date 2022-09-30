from aiogram.types import URLInputFile


def get_avatar(url):
    if not url:
        url = 'https://petrovka-38.com/images/petrovka/2017/1/9/115344820161227.jpg'
    avatar = URLInputFile(url)
    return avatar


def get_photo(url):
    if not url:
        url = 'https://t4.ftcdn.net/jpg/04/70/29/97/240_F_470299797_UD0eoVMMSUbHCcNJCdv2t8B2g1GVqYgs.jpg'
    else:
        url = f'http://192.241.142.246{url}'
    photo = URLInputFile(url)
    return photo
