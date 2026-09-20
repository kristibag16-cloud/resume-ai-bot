from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.states import ResumeStates
from bot.keyboards.inline import main_menu_kb, skip_vacancy_kb
from services.gigachat import GigaChatService

router = Router(name="resume")
gigachat = GigaChatService()


@router.message(ResumeStates.waiting_for_resume)
async def process_resume(message: Message, state: FSMContext):
    if not message.text or len(message.text) < 50:
        await message.answer(
            "Резюме слишком короткое. Пожалуйста, отправь полный текст резюме."
        )
        return

    data = await state.get_data()
    need_vacancy = data.get("need_vacancy", False)

    await state.update_data(resume_text=message.text)

    if need_vacancy:
        await state.set_state(ResumeStates.waiting_for_vacancy)
        await message.answer(
            "Теперь отправь текст вакансии, под которую нужно адаптировать резюме.\n\n"
            "Или нажми кнопку ниже, если хочешь просто улучшить резюме без вакансии.",
            reply_markup=skip_vacancy_kb()
        )
    else:
        await message.answer("Улучшаю резюме, подожди 10–20 секунд...")
        try:
            result = await gigachat.improve_resume(message.text)
            await message.answer(
                f"<b>Улучшенное резюме:</b>\n\n{result}",
                parse_mode="HTML"
            )
            await message.answer(
                "Что дальше?",
                reply_markup=main_menu_kb()
            )
        except Exception as e:
            await message.answer(
                "Произошла ошибка при обработке. Попробуй ещё раз немного позже."
            )
            print(f"Ошибка GigaChat: {e}")
        
        await state.clear()


@router.message(ResumeStates.waiting_for_vacancy)
async def process_vacancy(message: Message, state: FSMContext):
    if not message.text or len(message.text) < 30:
        await message.answer("Текст вакансии слишком короткий. Отправь более подробное описание.")
        return

    data = await state.get_data()
    resume_text = data.get("resume_text")

    await message.answer("Адаптирую резюме под вакансию, подожди 15–25 секунд...")

    try:
        result = await gigachat.improve_resume(resume_text, message.text)
        await message.answer(
            f"<b>Адаптированное резюме:</b>\n\n{result}",
            parse_mode="HTML"
        )
        await message.answer(
            "Что дальше?",
            reply_markup=main_menu_kb()
        )
    except Exception as e:
        await message.answer(
            "Произошла ошибка при обработке. Попробуй ещё раз немного позже."
        )
        print(f"Ошибка GigaChat: {e}")

    await state.clear()


@router.callback_query(F.data == "skip_vacancy")
async def skip_vacancy_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    resume_text = data.get("resume_text")

    await callback.message.edit_text("Улучшаю резюме, подожди 10–20 секунд...")

    try:
        result = await gigachat.improve_resume(resume_text)
        await callback.message.answer(
            f"<b>Улучшенное резюме:</b>\n\n{result}",
            parse_mode="HTML"
        )
        await callback.message.answer(
            "Что дальше?",
            reply_markup=main_menu_kb()
        )
    except Exception as e:
        await callback.message.answer(
            "Произошла ошибка при обработке. Попробуй ещё раз немного позже."
        )
        print(f"Ошибка GigaChat: {e}")

    await state.clear()
    await callback.answer()