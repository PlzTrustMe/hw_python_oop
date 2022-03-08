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
from math import pow


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

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

    LEN_STEP = 0.65
    M_IN_KM = 1000

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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float):
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        first_calorie_index = 18
        second_calorie_index = 20

        return ((first_calorie_index * self.get_mean_speed()
                 - second_calorie_index) * self.weight
                / self.M_IN_KM * (self.duration * 60))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        first_calorie_index = 0.035
        second_calorie_index = 0.029

        return (first_calorie_index * self.weight + (
                pow(self.get_mean_speed(), 2) // self.height)
                * second_calorie_index * self.weight) * (self.duration * 60)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

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

        return (self.get_mean_speed() + 1.1) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    class_data = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking
    }

    return class_data[workout_type](*data)


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
