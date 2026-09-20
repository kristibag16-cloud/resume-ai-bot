from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline import main_menu_kb
from bot.states import ResumeStates

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Привет! Я помогу профессионально улучшить твоё резюме.\n\n"
        "Выбери действие:",
        reply_markup=main_menu_kb()
    )


@router.callback_query(F.data == "improve_resume")
async def improve_resume_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ResumeStates.waiting_for_resume)
    await state.update_data(need_vacancy=False)
    
    await callback.message.edit_text(
        "Отправь текст своего резюме одним сообщением."
    )
    await callback.answer()


@router.callback_query(F.data == "adapt_resume")
async def adapt_resume_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ResumeStates.waiting_for_resume)
    await state.update_data(need_vacancy=True)
    
    await callback.message.edit_text(
        "Отправь текст своего резюме одним сообщением."
    )
    await callback.answer()