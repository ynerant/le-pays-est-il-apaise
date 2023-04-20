#!/usr/bin/env python3

from datetime import date, timedelta
import json
import os.path
import requests

from jinja2 import Environment, FileSystemLoader


BASE_DATE = date(2023, 4, 17)

def to_date(offset: int, date_format="%d/%m/%Y"):
    return (BASE_DATE + timedelta(days=offset)).strftime(date_format)


def generate():
    if not os.path.exists('output'):
        os.mkdir('output')

    if not os.path.exists('output/subtitles'):
        os.mkdir('output/subtitles')

    with open('data.json') as f:
        data = json.load(f)

    for day in data:
        for event in day['events']:
            for medium in event['media']:
                if 'subtitles_link' in medium:
                    req = requests.get(medium['subtitles_link'], stream=True)

                    with open(os.path.join('output/subtitles', medium['subtitles_file']), 'wb') as f:
                        for chunk in req.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)

    env = Environment(loader=FileSystemLoader("templates/"))
    env.filters['to_date'] = to_date
    template = env.get_template("template.html.j2")

    with open('output/index.html', 'w') as f:
        f.write(template.render(data=data, current_day=(date.today() - BASE_DATE).days))


if __name__ == '__main__':
    generate()
