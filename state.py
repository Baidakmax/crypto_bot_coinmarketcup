from aiogram.fsm.state import State, StatesGroup


class CryptoStates(StatesGroup):
    """
    # Define FSM states
    """
    waiting_for_crypto_name_10 = State()
    waiting_for_crypto_name_100 = State()