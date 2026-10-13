import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import counter_wardrobes_bot_token


# ==========================================
# НАСТРОЙКИ
# ==========================================

bot = Bot(token=counter_wardrobes_bot_token)
dp = Dispatcher()


# ==========================================
# СОСТОЯНИЯ
# ==========================================

class Cabinet(StatesGroup):
    # Цены материалов
    dsp_price = State()
    hdf_price = State()
    mdf_price = State()

    # Габариты шкафа
    height = State()
    width = State()
    depth = State()


# ==========================================
# START
# ==========================================

@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):

    await state.clear()

    await message.answer(
        "Привет! 👋\n\n"
        "Я помогу рассчитать стоимость материалов для шкафа.\n\n"
        "Сначала введём цены материалов.\n\n"
        "Введите цену ДСП за 1 м²:"
    )

    await state.set_state(Cabinet.dsp_price)


# ==========================================
# ЦЕНА ДСП
# ==========================================

@dp.message(Cabinet.dsp_price)
async def get_dsp_price(message: types.Message, state: FSMContext):

    try:
        price = float(message.text.replace(",", "."))

        if price <= 0:
            raise ValueError

    except ValueError:
        await message.answer(
            "❌ Некорректная цена.\n\n"
            "Введите число, например: 900"
        )
        return

    await state.update_data(dsp_price=price)

    await message.answer(
        "Цена ДСП сохранена ✅\n\n"
        "Введите цену ХДФ за 1 м²:"
    )

    await state.set_state(Cabinet.hdf_price)


# ==========================================
# ЦЕНА ХДФ
# ==========================================

@dp.message(Cabinet.hdf_price)
async def get_hdf_price(message: types.Message, state: FSMContext):

    try:
        price = float(message.text.replace(",", "."))

        if price <= 0:
            raise ValueError

    except ValueError:
        await message.answer(
            "❌ Некорректная цена.\n\n"
            "Введите число, например: 500"
        )
        return

    await state.update_data(hdf_price=price)

    await message.answer(
        "Цена ХДФ сохранена ✅\n\n"
        "Введите цену МДФ за 1 м²:"
    )

    await state.set_state(Cabinet.mdf_price)


# ==========================================
# ЦЕНА МДФ
# ==========================================

@dp.message(Cabinet.mdf_price)
async def get_mdf_price(message: types.Message, state: FSMContext):

    try:
        price = float(message.text.replace(",", "."))

        if price <= 0:
            raise ValueError

    except ValueError:
        await message.answer(
            "❌ Некорректная цена.\n\n"
            "Введите число, например: 1500"
        )
        return

    await state.update_data(mdf_price=price)

    await message.answer(
        "Цена МДФ сохранена ✅\n\n"
        "Теперь введём размеры шкафа.\n\n"
        "Введите ВЫСОТУ шкафа в миллиметрах.\n"
        "Например: 2400"
    )

    await state.set_state(Cabinet.height)


# ==========================================
# ВЫСОТА
# ==========================================

@dp.message(Cabinet.height)
async def get_height(message: types.Message, state: FSMContext):

    try:
        height = float(message.text.replace(",", "."))

        if height <= 0:
            raise ValueError

    except ValueError:
        await message.answer(
            "❌ Некорректная высота.\n\n"
            "Введите размер в миллиметрах.\n"
            "Например: 2400"
        )
        return

    await state.update_data(height=height)

    await message.answer(
        "Высота сохранена ✅\n\n"
        "Введите ШИРИНУ шкафа в миллиметрах.\n"
        "Например: 1800"
    )

    await state.set_state(Cabinet.width)


# ==========================================
# ШИРИНА
# ==========================================

@dp.message(Cabinet.width)
async def get_width(message: types.Message, state: FSMContext):

    try:
        width = float(message.text.replace(",", "."))

        if width <= 0:
            raise ValueError

    except ValueError:
        await message.answer(
            "❌ Некорректная ширина.\n\n"
            "Введите размер в миллиметрах.\n"
            "Например: 1800"
        )
        return

    await state.update_data(width=width)

    await message.answer(
        "Ширина сохранена ✅\n\n"
        "Введите ГЛУБИНУ шкафа в миллиметрах.\n"
        "Например: 600"
    )

    await state.set_state(Cabinet.depth)


# ==========================================
# ГЛУБИНА
# ==========================================

@dp.message(Cabinet.depth)
async def get_depth(message: types.Message, state: FSMContext):

    try:
        depth = float(message.text.replace(",", "."))

        if depth <= 0:
            raise ValueError

    except ValueError:
        await message.answer(
            "❌ Некорректная глубина.\n\n"
            "Введите размер в миллиметрах.\n"
            "Например: 600"
        )
        return

    await state.update_data(depth=depth)

    # ==========================================
    # ПОЛУЧАЕМ ВСЕ ДАННЫЕ
    # ==========================================

    data = await state.get_data()

    dsp_price = data["dsp_price"]
    hdf_price = data["hdf_price"]
    mdf_price = data["mdf_price"]

    height_mm = data["height"]
    width_mm = data["width"]
    depth_mm = data["depth"]

    # ==========================================
    # ПЕРЕВОДИМ ММ В МЕТРЫ
    # ==========================================

    height = height_mm / 1000
    width = width_mm / 1000
    depth = depth_mm / 1000

    # ==========================================
    # РАСЧЁТ ПЛОЩАДИ ДСП
    # ==========================================

    # Две боковины
    side_area = 2 * (height * depth)

    # Верх и низ
    top_bottom_area = 2 * (width * depth)

    # Передняя и задняя части короба
    front_back_area = 2 * (width * height)

    # Общая площадь ДСП
    dsp_area = (
        side_area
        + top_bottom_area
        + front_back_area
    )

    # ==========================================
    # РАСЧЁТ ХДФ
    # ==========================================

    # Задняя стенка
    hdf_area = width * height

    # ==========================================
    # РАСЧЁТ МДФ
    # ==========================================

    # Один фасад
    mdf_area = width * height

    # ==========================================
    # СТОИМОСТЬ
    # ==========================================

    dsp_cost = dsp_area * dsp_price
    hdf_cost = hdf_area * hdf_price
    mdf_cost = mdf_area * mdf_price

    total_cost = (
        dsp_cost
        + hdf_cost
        + mdf_cost
    )

    total_area = (
        dsp_area
        + hdf_area
        + mdf_area
    )

    # ==========================================
    # РЕЗУЛЬТАТ
    # ==========================================

    await message.answer(
        "📋 РАСЧЁТ ШКАФА\n\n"

        "📏 Габариты:\n"
        f"Высота: {height_mm:.0f} мм\n"
        f"Ширина: {width_mm:.0f} мм\n"
        f"Глубина: {depth_mm:.0f} мм\n\n"

        "━━━━━━━━━━━━━━━━━━\n\n"

        "🟫 ДСП:\n"
        f"Площадь: {dsp_area:.2f} м²\n"
        f"Цена: {dsp_price:.2f} руб./м²\n"
        f"Стоимость: {dsp_cost:.2f} руб.\n\n"

        "⬜ ХДФ:\n"
        f"Площадь: {hdf_area:.2f} м²\n"
        f"Цена: {hdf_price:.2f} руб./м²\n"
        f"Стоимость: {hdf_cost:.2f} руб.\n\n"

        "🟨 МДФ:\n"
        f"Площадь: {mdf_area:.2f} м²\n"
        f"Цена: {mdf_price:.2f} руб./м²\n"
        f"Стоимость: {mdf_cost:.2f} руб.\n\n"

        "━━━━━━━━━━━━━━━━━━\n\n"

        f"📐 Общая площадь материалов: "
        f"{total_area:.2f} м²\n"

        f"💰 Стоимость материалов: "
        f"{total_cost:.2f} руб."
    )

    # Очищаем состояние
    await state.clear()


# ==========================================
# ЗАПУСК
# ==========================================

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())