import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def generate_time_series(start_date: str = "2024-01-01",
                         periods: int = 100,
                         freq: str = "D",
                         value_min: float = 0.0,
                         value_max: float = 1.0) -> pd.DataFrame:
    """
    Генерация синтетического временного ряда.

    Параметры
    ----------
    start_date : Начальная дата (формат 'YYYY-MM-DD').
    periods : Количество временных точек.
    freq : Частота.
    value_min : Минимальное значение случайных чисел.
    value_max : Максимальное значение случайных чисел.

    Возращает таблицу с двумя колонками: 'date' и 'value'.
    """


    if periods <= 0:
        raise ValueError("Параметр 'periods' должен быть положительным числом.")
    if value_min >= value_max:
        raise ValueError("value_min должен быть меньше value_max.")

    # Создание временной оси
    dates = pd.date_range(start=start_date, periods=periods, freq=freq)

    # Генерация случайных значений
    values = np.random.uniform(low=value_min, high=value_max, size=periods)

    return pd.DataFrame({"date": dates, "value": values})


def plot_time_series(data: pd.DataFrame, title: str = "Синтетический временной ряд") -> None:
    """
    функция создает график со случкайными значениями по Y и временем по X


    параметры

    data : Таблица с колонками 'date' и 'value'.
    title : Заголовок графика.
    """

    if not {"date", "value"}.issubset(data.columns):
        raise ValueError("DataFrame должен содержать колонки 'date' и 'value'.")

    plt.figure(figsize=(12, 6))
    plt.plot(data["date"], data["value"], marker="o", linestyle="-", color="blue", label="Value")
    plt.title(title)
    plt.xlabel("Дата")
    plt.ylabel("Значение")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Пример использования
    ts_data = generate_time_series(start_date="2024-01-01", periods=50, freq="D", value_min=10, value_max=100)
    plot_time_series(ts_data)
