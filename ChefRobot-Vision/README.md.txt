# 🤖 Шеф-робот: система компьютерного зрения

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![YOLO](https://img.shields.io/badge/YOLO-v8-green.svg)](https://ultralytics.com)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-red.svg)](https://opencv.org)
[![Cursor](https://img.shields.io/badge/Cursor-AI--assisted-purple.svg)](https://cursor.sh)

## 🍳 О проекте

**ChefRobot-Vision** — это система компьютерного зрения для робота-повара. Она распознаёт продукты и кухонную утварь в реальном времени.

Проект создан для конкурса НИРС-2026 (ВолгГТУ) и демонстрирует интеграцию технологий искусственного интеллекта в робототехнику.

## ✨ Возможности

| Функция | Описание |
|---------|----------|
| 🍎 Распознавание | 100+ объектов: фрукты, овощи, посуда, готовая еда |
| ⚡ Скорость | Оптимизированная модель YOLOv8n для работы в реальном времени |
| 📸 Сохранение | Автоматическое сохранение фото при обнаружении объектов |
| ⌨️ Управление | Горячие клавиши для ручного управления |

## 🛠️ Установка

```bash
# Клонируем репозиторий
git clone https://github.com/Ilentuz/ChefRobot-Vision.git
cd ChefRobot-Vision

# Создаём виртуальное окружение
python -m venv chef_env
source chef_env/bin/activate  # Linux/Mac
chef_env\Scripts\activate     # Windows

# Устанавливаем зависимости
python -m pip install -r requirements.txt

                                                   🚀 Запуск
                                               python food_camera.py