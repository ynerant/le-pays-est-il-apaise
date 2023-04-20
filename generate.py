#!/usr/bin/env python3

from datetime import date, timedelta
import json

from jinja2 import Environment, FileSystemLoader


BASE_DATE = date(2023, 4, 17)

def to_date(offset: int, date_format="%d/%m/%Y"):
    return (BASE_DATE + timedelta(days=offset)).strftime(date_format)


def generate():
    with open('data.json') as f:
        data = json.load(f)

    env = Environment(loader=FileSystemLoader("templates/"))
    env.filters['to_date'] = to_date
    template = env.get_template("template.html.j2")

    with open('output/index.html', 'w') as f:
        f.write(template.render(data=data))


if __name__ == '__main__':
    generate()
