from aiogram.utils.i18n import gettext as _


def get_purpose(value):
    if value == 'apartment':
        return _('Квартира')
    if value == 'new_building':
        return _('Новострой')
    if value == 'cottage':
        return _('Коттедж')
