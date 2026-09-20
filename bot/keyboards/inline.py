from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Улучшить резюме",
            callback_data="improve_resume"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Адаптировать под вакансию",
            callback_data="adapt_resume"
        )
    )
    return builder.as_markup()


def skip_vacancy_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Пропустить (просто улучшить)",
            callback_data="skip_vacancy"
        )
    )
    return builder.as_markup()