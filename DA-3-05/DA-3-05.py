import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import argparse

# =========================
# 1. Создание синтетического временного ряда
# =========================
def create_synthetic_series(n_points: int, start_date: str = '2024-01-01') -> pd.DataFrame:
    """
    Генерирует синтетический временной ряд с датами и случайными значениями.

    Args:
        n_points (int): количество точек временного ряда (>0)
        start_date (str): дата начала ряда в формате 'YYYY-MM-DD'

    Returns:
        pd.DataFrame: DataFrame с колонками 'date' и 'value'
    """
    if n_points <= 0:
        raise ValueError("Количество точек должно быть положительным")

    np.random.seed(42)
    dates = pd.date_range(start=start_date, periods=n_points, freq='D')
    values = np.random.randint(10, 100, size=n_points)
    return pd.DataFrame({'date': dates, 'value': values})

# =========================
# 2. Скользящие статистики (DA-2-12)
# =========================
def calculation_moving_average(df: pd.DataFrame, windows: list, value_col: str = 'value', new_col: str = 'mov_avg') -> pd.DataFrame:
    """
    Вычисляет скользящее среднее для указанных окон.

    Args:
        df (pd.DataFrame)
        windows (list): размеры окон
        value_col (str): колонка с числовыми значениями
        new_col (str): базовое имя для новых столбцов

    Returns:
        pd.DataFrame: DataFrame с новыми колонками
    """
    df = df.copy()
    for window in windows:
        if window <= 0:
            raise ValueError("Размер окна должен быть положительным")
        df[f'{new_col}_{window}'] = df[value_col].rolling(window=window, min_periods=1).mean()
    return df

def calculation_moving_std(df: pd.DataFrame, windows: list, value_col: str = 'value', new_col: str = 'mov_std') -> pd.DataFrame:
    """
    Вычисляет скользящее стандартное отклонение для указанных окон.
    """
    df = df.copy()
    for window in windows:
        if window <= 0:
            raise ValueError("Размер окна должен быть положительным")
        df[f'{new_col}_{window}'] = df[value_col].rolling(window=window, min_periods=1).std()
    return df

def calculation_count_over_threshold(df: pd.DataFrame, windows: list, value_col: str = 'value', new_col: str = 'count_thr', threshold: float = 50) -> pd.DataFrame:
    """
    Вычисляет количество значений > threshold в каждом скользящем окне.
    """
    df = df.copy()
    for window in windows:
        if window <= 0:
            raise ValueError("Размер окна должен быть положительным")
        df[f'{new_col}_{window}'] = df[value_col].rolling(window=window, min_periods=1)\
            .apply(lambda x: (x > threshold).sum(), raw=False)
    return df

# =========================
# 3. Скользящее количество > локального среднего (DA-2-28)
# =========================
def calculation_count_above_mean(df: pd.DataFrame, windows: list, value_col: str = 'value', new_col: str = 'count_above_mean') -> pd.DataFrame:
    """
    Вычисляет количество значений в окне, которые больше среднего по окну.
    """
    df = df.copy()
    def count_above_mean(x):
        return np.sum(x > x.mean())

    for window in windows:
        if window <= 0:
            raise ValueError("Размер окна должен быть положительным")
        df[f'{new_col}_{window}'] = df[value_col].rolling(window=window, min_periods=1)\
            .apply(count_above_mean, raw=False)
    return df

# =========================
# 4. Визуализация
# =========================
def build_graph(df: pd.DataFrame, windows: list, output_dir: str = 'output', format_file: str = 'png'):
    """
    Строит три отдельных графика по очереди:
    1) Исходный ряд + скользящие средние
    2) Count > threshold
    3) Count > rolling mean
    """

    # --------------------
    # 1. Основной ряд + скользящие средние
    # --------------------
    plt.figure(figsize=(12,6))
    plt.plot(df['date'], df['value'], label='Value', color='black', linewidth=2)
    for window in windows:
        plt.plot(df['date'], df[f'mov_avg_{window}'], label=f'Moving Avg {window}')
    plt.title('Исходный ряд + скользящие средние')
    plt.xlabel('Дата')
    plt.ylabel('Значения')
    plt.grid(alpha=0.3)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Сохранение
    try:
        output_path = Path(output_dir) / f"mov_avg_plot.{format_file}"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, format=format_file, dpi=300)
    except Exception as e:
        print(f"Ошибка при сохранении графика: {e}")
    plt.show()

    # --------------------
    # 2. Count > threshold
    # --------------------
    plt.figure(figsize=(12,6))
    for window in windows:
        plt.plot(df['date'], df[f'count_thr_{window}'], label=f'Count > Threshold {window}', linestyle='--', color='green')
    plt.title('Количество значений > порога')
    plt.xlabel('Дата')
    plt.ylabel('Счётчик')
    plt.grid(alpha=0.3)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    try:
        output_path = Path(output_dir) / f"count_threshold_plot.{format_file}"
        plt.savefig(output_path, format=format_file, dpi=300)
    except Exception as e:
        print(f"Ошибка при сохранении графика: {e}")
    plt.show()

    # --------------------
    # 3. Count > rolling mean
    # --------------------
    plt.figure(figsize=(12,6))
    for window in windows:
        plt.plot(df['date'], df[f'count_above_mean_{window}'], label=f'Count > Mean {window}', linestyle='-.', color='red')
    plt.title('Количество значений > локального среднего')
    plt.xlabel('Дата')
    plt.ylabel('Счётчик')
    plt.grid(alpha=0.3)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    try:
        output_path = Path(output_dir) / f"count_above_mean_plot.{format_file}"
        plt.savefig(output_path, format=format_file, dpi=300)
    except Exception as e:
        print(f"Ошибка при сохранении графика: {e}")
    plt.show()

# =========================
# 5. Основной блок
# =========================
def main():
    parser = argparse.ArgumentParser(description='DA-3-05: интеграция DA-2-12 и DA-2-28')
    parser.add_argument('-n', '--n-points', type=int, default=60, help='Количество точек')
    parser.add_argument('-w', '--windows', nargs='+', type=int, default=[3,5,7], help='Окна')
    parser.add_argument('-t', '--threshold', type=float, default=50, help='Порог для счётчика')
    parser.add_argument('-o', '--output', default='output', help='Папка для графика')
    parser.add_argument('--format', default='png', choices=['png','pdf','jpg'], help='Формат файла')
    args = parser.parse_args()

    try:
        df = create_synthetic_series(args.n_points)
        df = calculation_moving_average(df, args.windows)
        df = calculation_moving_std(df, args.windows)
        df = calculation_count_over_threshold(df, args.windows, threshold=args.threshold)
        df = calculation_count_above_mean(df, args.windows)
        build_graph(df, args.windows, args.output, args.format)
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
