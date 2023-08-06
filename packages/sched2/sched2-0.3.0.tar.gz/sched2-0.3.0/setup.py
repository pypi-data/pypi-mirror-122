# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sched2']
setup_kwargs = {
    'name': 'sched2',
    'version': '0.3.0',
    'description': 'Event scheduler 2',
    'long_description': '# Event scheduler 2\n\n`sched2`\' provides a *subclass* of `sched.scheduler` with extra functionality.\nIf you\'re already using `sched` then `sched2` is a drop-in-place change.\n\n## The extra functionality\n- `enter` - now also accepts `datetime.timedelta` objects as values for the delta parameter.\n- `repeat` - a new method with the same signature as `enter` that re-schedules `action` after it returns.\n- `every` -  is a decorator variant of `repeat` that schedules the decorated function at definition time.\n\n ### Enter\nSchedules an `action` to be called only once after some `delay` whereas `repeat` will re-schedule the `action` to be called again and again forever. It does this by repeatedly pushing the `action` *callable* back into the scheduler queue. The `delay` and `priority` values are fixed for all reintroductions into the queue.\n\n### Every\nA decorator that provides a friendly way of scheduling functions at definition time.\n\n\n## Install\n\n`pip install sched2`\n\n\n## Use\n\n\n```python\nfrom urllib.request import urlopen\nfrom sched2 import scheduler\n\n\nsc = scheduler()\n\n\n# repeatedly print public IP every 60 seconds\n@sc.every(60, 0)\ndef echo_ip():\n    ip = urlopen("https://icanhazip.com/").read().decode("utf-8").strip()\n    print(f"ip: {ip}")\n\nsc.run()\n```\n\n\nNow a less realistic example showing all the extra functionality\n\n```python\nfrom time import time\nfrom datetime import datetime, timedelta\n\nfrom sched2 import scheduler\n\n\nstarted_at = time()\n\n# we\'ll use this in a bit\ndef echo_time_elapsed():\n    seconds_since_started = round(time() - started_at, 2)\n    print(f"started {seconds_since_started}s ago")\n\n\nprint(f"started at {started_at}")\n\n\n# create a scheduler object\nsc = scheduler()\n\n\n# schedule calling a function repeatedly\n# with a delay of 10 seconds between calls\nsc.repeat(delay=10, priority=1, action=echo_time_elapsed)\n\n\n# schedule a funcion by decorating it\n@sc.every(delay=15, priority=0)\ndef print_current_time():\n    iso_dt = datetime.utcnow().isoformat()\n    print(f"decorated function - {iso_dt}")\n\n\n# you can also use datetime.timedelta objects\n# see: https://docs.python.org/3/library/datetime.html#timedelta-objects\n@sc.every(delay=timedelta(minutes=1), priority=0)\ndef echo_iso_date_every_minute():\n    iso_dt = datetime.utcnow().isoformat()\n    print(f"decorated function with timedelta - {iso_dt}")\n\n\n# run the scheduler\nsc.run()\n```\n',
    'author': 'Pedro Rodrigues',
    'author_email': 'medecau@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/medecau/sched2',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
