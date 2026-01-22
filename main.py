from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.uix.button import Button
import os


class BackgroundApp(App):
    def build(self):
        # Настройки окна - фиксированный размер 700x360
        Window.size = (700, 360)
        Window.minimum_width, Window.minimum_height = Window.size
        Window.maximum_width, Window.maximum_height = Window.size

        # Создаем главный контейнер
        self.layout = BoxLayout(orientation='vertical')

        # Полные пути к изображениям
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Список фоновых изображений
        self.backgrounds = [
            os.path.join(current_dir, 'source/ex/main.jpg'),
            os.path.join(current_dir, 'source/ex/main1.jpg'),
        ]
        self.current_bg = 0

        # Добавляем фон в canvas.before
        with self.layout.canvas.before:
            # Берём первый найденный фон или пустую строку
            first_bg = next((bg for bg in self.backgrounds if os.path.exists(bg)), '')
            self.bg = Rectangle(
                source=first_bg,
                size=Window.size,
                pos=self.layout.pos
            )

        # Верхняя пустая область (80% высоты)
        self.layout.add_widget(BoxLayout(size_hint=(1, 0.8)))

        # Контейнер для кнопки в самом центре нижней части (20% высоты)
        button_container = BoxLayout(
            size_hint=(1, 0.2),  # 20% высоты
            padding=0,
            orientation='vertical'
        )

        # Пустое пространство над кнопкой для вертикального центрирования
        button_container.add_widget(BoxLayout(size_hint=(1, 0.5)))

        # Контейнер для горизонтального центрирования кнопки
        button_inner = BoxLayout(
            size_hint=(1, 0.5),  # Половина контейнера для кнопки
            padding=50  # Отступы по бокам
        )

        # Создаём кнопку-иконку
        icon_normal = os.path.join(current_dir, 'source/ex/logo.png')
        icon_down = os.path.join(current_dir, 'source/ex/logo.png')

        # Создаём кнопку
        self.button = Button(
            size_hint=(None, None),
            size=(70, 70),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},  # Полное центрирование
            background_normal=icon_normal if os.path.exists(icon_normal) else '',
            background_down=icon_down if os.path.exists(icon_down) else '',
            border=(0, 0, 0, 0)
        )

        # Привязка события клика
        self.button.bind(on_press=self.change_background)

        # Добавляем кнопку в контейнер
        button_inner.add_widget(BoxLayout())  # Левое пространство
        button_inner.add_widget(self.button)
        button_inner.add_widget(BoxLayout())  # Правое пространство

        button_container.add_widget(button_inner)
        self.layout.add_widget(button_container)

        return self.layout

    def change_background(self, instance):
        """Изменяет фон на следующий в списке"""
        if not hasattr(self, 'backgrounds') or len(self.backgrounds) == 0:
            print("Ошибка: нет доступных фонов")
            return

        # Ищем следующий существующий фон
        found = False
        for i in range(len(self.backgrounds)):
            self.current_bg = (self.current_bg + 1) % len(self.backgrounds)
            bg_path = self.backgrounds[self.current_bg]
            if os.path.exists(bg_path):
                self.bg.source = bg_path
                print(f"✓ Фон изменен на: {os.path.basename(bg_path)}")
                found = True
                break

        if not found:
            print("Не найден ни один существующий фон")

    def on_start(self):
        """Вызывается при старте приложения"""
        # Принудительное обновление фона
        self.bg.size = Window.size
        self.bg.pos = self.layout.pos
        print("\nПриложение запущено! Нажмите на кнопку для смены фона.")


if __name__ == '__main__':
    BackgroundApp().run()