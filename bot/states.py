from aiogram.fsm.state import State, StatesGroup


class ResumeStates(StatesGroup):
    waiting_for_resume = State()
    waiting_for_vacancy = State()