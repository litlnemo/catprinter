import sys
import datetime 
import python_weather
import asyncio
import os
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont

# Constants
PRINTER_WIDTH = 384

# Get the current date and time
date = datetime.datetime.now()
time = date.strftime('%x %I:%M%p')

def create_text(text, font_name="DejaVuSans-Bold.ttf", font_size=25):
    lines = text.splitlines()

    pic = PIL.Image.open("media/catprinter.jpg")

    # Resize the image proportionally if its width is greater than PRINTER_WIDTH
    if pic.width > PRINTER_WIDTH:
        scaling_factor = PRINTER_WIDTH / float(pic.width)
        new_height = int(pic.height * scaling_factor)
        pic = pic.resize((PRINTER_WIDTH, new_height), PIL.Image.Resampling.LANCZOS)
    else:
        new_height = pic.height

    # Create a new blank image with white background
    height = (len(lines) * font_size) + new_height + 100
    img = PIL.Image.new('RGB', (PRINTER_WIDTH, height), color=(255, 255, 255))

    # Center the image horizontally
    x_position = (PRINTER_WIDTH - pic.width) // 2
    img.paste(pic, (x_position, 0))

    # Draw the text below the image
    font = PIL.ImageFont.truetype(font_name, font_size)
    d = PIL.ImageDraw.Draw(img)

    y_position = new_height + 10
    for line in lines:
        d.text((PRINTER_WIDTH // 2, y_position), line, fill=(0, 0, 0), font=font, anchor='ma')
        y_position += font_size + 10

    img.save("weather.png")

def greeting():
    # Simple greeting based on time of day
    hour = datetime.datetime.now().hour
    if 3 <= hour < 12:
        return "morning"
    elif 12 <= hour < 18:
        return "afternoon"
    elif 18 <= hour < 21:
        return "evening"
    else:
        return "night"

async def get_weather():
    
    # Fetch the weather forecast
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        weather = await client.get(city)
        return [weather.description, weather.temperature, weather.kind.emoji]

if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    city = input("What city? ")
    current_weather = asyncio.run(get_weather())
    weather_info = f"Good {greeting()}!\nCurrent weather\nin {city} is:\n{current_weather[0]} & {current_weather[1]}F\n{time}"
    create_text(weather_info)
