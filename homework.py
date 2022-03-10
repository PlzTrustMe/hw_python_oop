"""
Программный модуль фитнес-трекера, который обрабатывает данные для трех видов
тренировок: для бега, спортивной ходьбы и плавания.

Этот модуль:
    - Принимает от блока датчиков информацию о прошедшей тренировке.
    - Определяет вид тренировки.
    - Рассчитывает результаты тренировки.
    - Выводит информационное сообщение о результатах тренировки.

Информационное сообщение выводит:
    - Тип тренировки (бег, ходьба или плавание).
    - Длительность тренировки.
    - Дистанция, которую преодолел пользователь, в километрах.
    - Среднюю скорость на дистанции, в км/ч.
    - Расход энергии, в килокалориях.
"""
import numbers
from dataclasses import dataclass
from typing import Dict, List, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Функция выводит сообщения о результате тренировки."""

        return (
            f"Тип тренировки: {self.training_type}; "
            f"Длительность: {self.duration:.3f} ч.; "
            f"Дистанция: {self.distance:.3f} км; "
            f"Ср. скорость: {self.speed:.3f} км/ч; "
            f"Потрачено ккал: {self.calories:.3f}."
        )


class Training:
    """Базовый класс тренировки."""

    # Расстояние, которое спортсмен преодолевает за один шаг.
    LEN_STEP: float = 0.65
    # Константа для перевода значений из метров в километры.
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        # Ошибка когда производные методы перезаписывают оригинальный.
        raise NotImplementedError(f"{self.__class__.__name__} "
                                  "get_spent_calories")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    MULTIPLIER: int = 18  # Коэффициенты для расчёта формулы.
    SUBTRACTOR: int = 20
    MINUTE_PER_HOUR: int = 60  # Переменная для перевода часов в минуты.

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.MULTIPLIER * self.get_mean_speed()
                 - self.SUBTRACTOR) * self.weight
                / self.M_IN_KM * (self.duration * self.MINUTE_PER_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    DEGREE: int = 2  # Степень для формулы get_spent_calories().
    WEIGHT_MULTIPLIER: float = 0.035  # Коэффициенты для расчёта формулы.
    SQUARE_OF_SPEED_MULTIPLIER: float = 0.029
    MINUTE_PER_HOUR: int = 60  # Переменная для перевода часов в минуты.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.WEIGHT_MULTIPLIER * self.weight
                 + (pow(self.get_mean_speed(), self.DEGREE) // self.height)
                 * self.SQUARE_OF_SPEED_MULTIPLIER * self.weight)
                * (self.duration * self.MINUTE_PER_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""

    # Расстояние, которое спортсмен преодолевает за один гребок.
    LEN_STEP: float = 1.38
    ADDENDUM: float = 1.1  # Слогаемое.
    MULTIPLIER: int = 2  # Множитель.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.get_mean_speed() + self.ADDENDUM)
                * self.MULTIPLIER * self.weight)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    obj_code_data: Dict[str, Type[Training]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking
    }

    # Проверка на число, а так же корректный тип тренировки.
    if workout_type in obj_code_data and all(
            [isinstance(_, numbers.Number) for _ in data]):
        return obj_code_data[workout_type](*data)
    else:
        raise ValueError("Полученый тип или данные неккоректны!")


def main(exercise: Training) -> None:
    """Главная функция."""
    info = exercise.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for key, value in packages:
        training = read_package(key, value)
        main(training)
