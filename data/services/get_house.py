from aiogram.utils.i18n import gettext as _


def get_house(value):
    if int(value) == 1:
        return _('Ипатий')
    if int(value) == 2:
        return _('Ладислав')
