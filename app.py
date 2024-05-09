import json
from datetime import datetime, timedelta

from PIL import Image
import requests
import customtkinter

from .config import API_KEY


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.setup_ui()
        
        self.BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
        self.API_KEY = API_KEY

        

    def setup_ui(self):
        customtkinter.set_appearance_mode("System")  
        customtkinter.set_default_color_theme("dark-blue")

        self.title("Прогноз погоды")
        self.resizable(False, False)
        self.geometry("400x510")

        self.setup_logo()
        self.setup_city_entry()
        self.setup_button_get()
        self.setup_city_labels()



    def setup_logo(self):
        self.logo_img = customtkinter.CTkImage(
            light_image=Image.open("logo.webp"),
            dark_image=Image.open("logo.webp"),
            size=(70, 70)
        )
        
        self.logo = customtkinter.CTkLabel(self, image=self.logo_img, text="")
        self.logo.place(x=15, y=10)

        self.logo_text = customtkinter.CTkLabel(self, text="Прогноз погоды",
                                                 font=('Arial', 32))
        self.logo_text.place(x=90, y=25)

    def setup_city_entry(self):
        self.city_entry = customtkinter.CTkEntry(
            self, width=375, height=70,
            placeholder_text="Введите название города", font=("Arial", 28)
        )
        self.city_entry.place(x=15, y=80)

    def setup_button_get(self):
        self.button_get = customtkinter.CTkButton(
            self, text="Узнать погоду", width=375, height=70,
            font=("Arial", 32), command=self.button_weather_get
        )
        self.button_get.place(x=15, y=160)

    def setup_city_labels(self):
        self.city_name = customtkinter.CTkLabel(
            self, text="Введите название города", font=("Arial", 28)
        )
        self.city_name.place(x=15, y=250)

        self.city_description = customtkinter.CTkLabel(
            self, text="", justify="right", wraplength=140, font=("Arial", 24)
        )
        self.city_description.place(x=250, y=250)

        self.city_temp = customtkinter.CTkLabel(self, text="",
                                                font=("Arial", 24))
        self.city_temp.place(x=15, y=300)

        self.feels_like = customtkinter.CTkLabel(self, text="",
                                                 font=("Arial", 24))
        self.feels_like.place(x=15, y=335)

        self.speed_wind = customtkinter.CTkLabel(self, text="",
                                                 font=("Arial", 24))
        self.speed_wind.place(x=15, y=370)

        self.humidity = customtkinter.CTkLabel(self, text="",
                                               font=("Arial", 24))
        self.humidity.place(x=15, y=405)

        self.sunrise = customtkinter.CTkLabel(self, text="",
                                              font=("Arial", 24))
        self.sunrise.place(x=15, y=440)

        self.sunset = customtkinter.CTkLabel(self, text="",
                                             font=("Arial", 24))
        self.sunset.place(x=15, y=475)

    def button_weather_get(self):
        # Получаем данные о погоды
        weather_data = self.get_weather_data()
        
        # Если данные о погоде нет, пишем что такой город не найден
        if not weather_data:
            self.clear_labels()
            self.city_name.configure(text="Город не найден")
            return

        

        # Обновляем данные о погоде
        self.city_name.configure(text=self.city_entry.get().capitalize())

        # Очистка текстового поля
        self.city_entry.delete(0, customtkinter.END)
        
        self.city_description.configure(text=weather_data["description"])
        self.city_temp.configure(text=f"Температура: {weather_data['temp']}")
        self.feels_like.configure(
            text=f"Ощущается как: {weather_data['feels_like']}"
        )
        self.speed_wind.configure(
            text=f"Скорость ветра: {weather_data['speed_wind']}"
        )
        self.humidity.configure(text=f"Влажность: {weather_data['humidity']}")
        self.sunrise.configure(
            text=f"Восход солнца: {weather_data['sunrise']}"
        )
        self.sunset.configure(text=f"Заход солнца: {weather_data['sunset']}")

        
    def get_weather_data(self):
        # Получаем данные о погоде 
        req = requests.get(f"{self.BASE_URL}?q={self.city_entry.get()}&lang=ru&appid={self.API_KEY}")
        weather_data = json.loads(req.text)

        # Проверяем есть ли данные о погоде
        if weather_data["cod"] == "404":
            return None

        #Создаем словарь для хранения нужных данных о погоде
        result_data = {}

        
        #Определяем ключи которые нам нужны
        desired_keys = ["temp", "feels_like", "wind",
                        "sunrise", "sunset", "humidity", "description"]

        # Обрабатываем каждый ключ
        for key in desired_keys:
            if key == "wind":
                # Обрабатываем скорость ветра
                result_data["speed_wind"] = f"{weather_data[key]['speed'] } м/с"
            elif key == "description":
                # Добавляем описание погоды
                result_data[key] = weather_data["weather"][0][key]
            elif key in ["sunrise", "sunset"]:
                # Преобразуем время восхода изахода солнца из Unix времени в формат времени
                timezone = weather_data["timezone"] / 3600
                result_data[key] = (
                    datetime.fromtimestamp(
                    weather_data["sys"][key]) - timedelta(hours=3)
                )
                result_data[key] += timedelta(hours=timezone)
                result_data[key] = result_data[key].strftime("%H:%M")
                
            elif key in ["temp", "feels_like"]:
                # Преобразуем температуру в градусы цельсия
                result_data[key] = \
                                f"{int(weather_data['main'][key] - 273.15)}°C"
            else:
                # Обрабатываем влажность 
                result_data[key] = f"{weather_data['main']['humidity']}%"
                

        return result_data
            


    def clear_labels(self):
        self.city_description.configure(text="")

        self.city_temp.configure(text="")
        self.feels_like.configure(text="")

        self.speed_wind.configure(text="")
        self.humidity.configure(text="")

        self.sunrise.configure(text="")
        self.sunset.configure(text="")

        

        

    
app = App()
app.mainloop()
    