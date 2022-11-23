#!/usr/bin/env python3

import os
import i18n

from subtitld.modules.paths import PATH_SUBTITLD

i18n.set('file_format', 'json')
i18n.load_path.append(os.path.join(PATH_SUBTITLD, 'locale'))
i18n.set('filename_format', '{locale}.{format}')
i18n.set('skip_locale_root_data', True)
i18n.set('fallback', 'en_US')


def _(text):
    return i18n.t(text)


# LIST_OF_MONTHS = ['', _('January'), _('February'), _('March'), _('April'), _('May'), _('June'), _('July'), _('August'), _('September'), _('October'), _('November'), _('December')]
# LIST_OF_WEEKDAYS = [_('Monday'), _('Tuesday'), _('Wednesday'), _('Thursday'), _('Friday'), _('Saturday'), _('Sunday')]

# def translate_month_names():
#     global LIST_OF_MONTHS
#     LIST_OF_MONTHS = []
#     for item in ['', _('January'), _('February'), _('March'), _('April'), _('May'), _('June'), _('July'), _('August'), _('September'), _('October'), _('November'), _('December')]:
#         LIST_OF_MONTHS.append(_(item))


def load_translation_files():
    for lp in i18n.load_path:
        for f in os.listdir(lp):
            path = os.path.join(lp, f)
            if os.path.isfile(path) and path.endswith(i18n.config.get('file_format')):
                locale = f.split(i18n.config.get('namespace_delimiter'))[0]
                if '{locale}' in i18n.config.get('filename_format') and locale not in i18n.config.get('available_locales'):
                    i18n.resource_loader.load_translation_file(f, lp, locale)


# def get_list_of_months(language):
#     month_list = ['']
#     for month in LIST_OF_MONTHS:
#         if month:
#             month_list.append(i18n.t(month, locale=language))
#     return month_list


# def get_list_of_weekdays(language):
#     weekdays = []
#     for month in LIST_OF_WEEKDAYS:
#         if month:
#             weekdays.append(i18n.t(month, locale=language))
#     return weekdays


def set_language(language):
    i18n.set('locale', language)


def get_language_pairs(language):
    result = i18n.translations.container.get(language, {})
    return result


def get_available_language_names():
    final_dict = {}
    for language in i18n.translations.container:
        final_dict[language] = i18n.translations.container[language].get('language_name', '')
    return final_dict
