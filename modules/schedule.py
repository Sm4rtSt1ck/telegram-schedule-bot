from datetime import datetime
import csv
from os import getenv
import re

from dotenv import load_dotenv
from telebot import types


# Load environment variables from a specified .env file
load_dotenv("settings/lang.env")

WEEKDAYS = list(map(lambda day: day.replace("_", " "), getenv("WEEKDAYS").split()))


class Schedule:
    def __init__(self, file_name: str = "database/schedule.csv") -> None:
        self.__file_name = file_name
        self.__schedule: dict[str, list] = {}
        with open(self.__file_name, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    self.__schedule[row["Group"]].append([row["Day"], row["Time"], row["Subject"], row["Room"]])
                except KeyError:
                    self.__schedule[row["Group"]] = [[row["Day"], row["Time"], row["Subject"], row["Room"]]]

    def check_group(self, group: str) -> bool:
        """Check if the group exists in the schedule CSV file"""

        return group in self.__schedule

    def set_schedule(self, message: types.Message, group: str) -> bool:
        """Add a new schedule for a group, validating the input format"""

        schedule_entry = message.text.split("\n")

        # Check if the schedule entry matches the required format
        entry_pattern = re.compile(r'^\d\s*,\s*\d{2}:\d{2}-\d{2}:\d{2}\s*,[0-9a-zA-Zа-яА-Я\s]+, [0-9a-zA-Zа-яА-Я\s]+')
        new_schedule: list[list] = []
        for row in schedule_entry:
            if not entry_pattern.match(row):
                return False
            components = row.split(', ')
            day = int(components[0].strip())
            time = components[1].strip()
            subject = components[2].strip()
            room = components[3].strip()

            # Validate the day, subject, and room
            if not 1 <= day <= 7 or not subject or not room:
                return False

            # Append the validated schedule entries
            new_schedule.append([group, day, time, subject, room])

        # If all checks pass, append the schedule
        for row in new_schedule:
            try:
                self.__schedule[row[0]].append([row[1], row[2], row[3], row[4]])
            except KeyError:
                self.__schedule[row[0]] = [[row[1], row[2], row[3], row[4]]]

        with open(self.__file_name, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(new_schedule)
        
        return True

    def get_day(self, group: str) -> str:
        """Retrieve the schedule for the current day for a specific group"""

        schedule = []

        for couple in self.__schedule[group]:
            if couple[0] == str(datetime.now().weekday()+1):
                formatted_entry = f"`{couple[1]}`: {couple[2]}, _{couple[3]}_"
                schedule.append(formatted_entry)

        return f"*{WEEKDAYS[datetime.now().weekday()]}:*\n{'\n\n'.join(schedule)}" if schedule else getenv("NO_SCHEDULE")


    def get_week(self, group: str) -> str:
        """Retrieve the weekly schedule for a specific group"""

        schedule: dict[str, list[str]] = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: []}
        for couple in self.__schedule[group]:
            formatted_entry = f"`{couple[1]}`: {couple[2]}, _{couple[3]}_"
            schedule[int(couple[0])].append(formatted_entry)

        result = ""
        for day, day_schedule in schedule.items():
            result += f"*{WEEKDAYS[day-1]}:*\n"
            result += ("\n".join(day_schedule) if len
            (day_schedule) > 0 else getenv("NO_SCHEDULE")) + "\n\n"
        return result if schedule else getenv("NO_SCHEDULE")


    def get_session(self, group: str) -> str:
        """Retrieve the session schedule for a specific group (not yet implemented)"""

        return getenv("IN_DEVELOPING")
