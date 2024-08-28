import sys
import datetime 
import python_weather
import asyncio
import os
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import calendar
import random

# Constants
PRINTER_WIDTH = 384


# Get the current date and time
date = datetime.datetime.now()
time = date.strftime('%x %I:%M%p')
today = datetime.date.today()


# Generating calendar
text_calendar = calendar.TextCalendar()
text_calendar.setfirstweekday(calendar.SUNDAY)
cal = text_calendar.formatmonth(today.year, today.month)


def create_text_with_calendar(text, calendar_text, font_name="DejaVuSans-Bold.ttf", font_size=25, cal_font_name="DejaVuSansMono.ttf"):
    lines = text.splitlines()  # Split the text into lines

    # Generate random number for random picture choice
    # Pics are named "#.png" -- media folder currently hard-coded
    random_number = int(random.randrange(1, 14))
    pic = PIL.Image.open(f"media/{random_number}.png", "r")
    
    # Resize the image proportionally if its width is greater than 384px
    max_width = 384
    if pic.width > max_width:
        scaling_factor = max_width / float(pic.width)
        new_height = int(pic.height * scaling_factor)
        pic = pic.resize((max_width, new_height), PIL.Image.Resampling.LANCZOS)
    else:
        new_height = pic.height  # If the width is smaller, keep the original height

    # Calculate the height for the text
    text_height = len(lines) * (font_size + 10)

    # Estimate the height of the calendar
    cal_lines = calendar_text.splitlines()
    calendar_height = len(cal_lines) * (font_size - 5 + 10) + 20  # Added padding between text and calendar

    # Calculate the total height of the image
    height = new_height + text_height + calendar_height + 40  # Added extra space

    # Create a new blank image with the calculated height
    img = PIL.Image.new('RGB', (max_width, height), color=(255, 255, 255))
    
    # Center the image horizontally
    x_position = (max_width - pic.width) // 2
    img.paste(pic, (x_position, 0))
    
    # Draw the text below the image
    font = PIL.ImageFont.truetype(font_name, font_size)
    d = PIL.ImageDraw.Draw(img)
    
    y_position = new_height + 10  # Start drawing text below the image
    for line in lines:
        d.text((max_width // 2, y_position), line, fill=(0, 0, 0), font=font, anchor='ma')
        y_position += font_size + 10
    
    # Adding space before the calendar
    y_position += 20

    # Draw the calendar below the text
    cal_font = PIL.ImageFont.truetype(cal_font_name, font_size - 5)
    for cal_line in cal_lines:
        d.text((max_width // 2 - 5, y_position), cal_line, fill=(0, 0, 0), font=cal_font, anchor="ma")
        y_position += font_size - 5 + 10
    
    img.save("weathercalendar.png")



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
        return [weather.description, weather.temperature]
        # weather.kind.emoji was used to include an emoji, but doesn't work for certain forecasts

        

if __name__ == "__main__":
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    city = input("What city? ")
    current_weather = asyncio.run(get_weather())
    weather_info = f"Good {greeting()}!\nCurrent weather\nin {city} is:\n{current_weather[0]} & {current_weather[1]}F\n{time}"
    create_text_with_calendar(weather_info, calendar_text=cal)
