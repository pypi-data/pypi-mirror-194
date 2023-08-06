# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['connectsensor']

package_data = \
{'': ['*']}

install_requires = \
['async-property>=0.2.1,<0.3.0',
 'asyncio>=3.4.3,<4.0.0',
 'datetime>=4.7,<5.0',
 'httpx>=0.23.0,<0.24.0',
 'pandas>=1.4.3,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'zeep>=4.2.0,<5.0.0']

entry_points = \
{'console_scripts': ['kingspan-export = connectsensor._kingspan_export:main',
                     'kingspan-notifier = '
                     'connectsensor._kingspan_notifier:main',
                     'kingspan-status = connectsensor._kingspan_status:main']}

setup_kwargs = {
    'name': 'kingspan-connect-sensor',
    'version': '2.1.0',
    'description': 'API to get oil tank from Kingspan SENSiT sensors',
    'long_description': '# kingspan-connect-sensor\n\n[![build:](https://github.com/masaccio/kingspan-connect-sensor/actions/workflows/run-all-tests.yml/badge.svg)](https://github.com/masaccio/kingspan-connect-sensor/actions/workflows/run-all-tests.yml)\n[![build:](https://github.com/masaccio/kingspan-connect-sensor/actions/workflows/codeql.yml/badge.svg)](https://github.com/masaccio/kingspan-connect-sensor/actions/workflows/codeql.yml)\n<!-- [![codecov](https://codecov.io/gh/masaccio/kingspan-connect-sensor/branch/main/graph/badge.svg?token=EKIUFGT05E)](https://codecov.io/gh/masaccio/kingspan-connect-sensor) -->\n\nAPI to get oil tank from [Kingspan SENSiT sensors](https://www.kingspan.com/gb/en-gb/products/tank-monitoring-systems/remote-tank-monitoring/sensit-smart-wifi-tank-level-monitoring-kit)\n\nTo make use of the API, you will need the credentials you used to register with the App. You do not need other details such as the tank ID as these are already associated with your account.\n\n## Installation\n\n``` bash\npython3 -m pip kingspan-connect-sensor\n```\n\n## Usage\n\n*NOTE* from version 2.0.0, the API changes to use attributes rather than methods for tank parameters.\n\nReading documents:\n\n``` python\nfrom connectsensor import SensorClient\n\nclient = SensorClient()\nclient.login("test@example.com", "s3cret")\ntanks = client.tanks\ntank_level = tanks[0].level\n```\n\nThe `tanks` method returns a `Tanks` object which can be queried for the status of the specific tank.\n\n## Async Usage\n\nFrom version 2.0.0, an asyncio verison of the client is available:\n\n``` python\nasync with AsyncSensorClient() as client:\n    await client.login("test@example.com", "s3cret")\n    tanks = await client.tanks\n    tank_level = await tanks[0].level\n    tank_capcity = await tanks[0].capacity\n    tank_percent = 100 * (tank_level / tank_percent)\n    print(f"Tank is {tank_percent:.1f}% full")\n```\n\n## Tanks object\n\n`history` returns a Pandas dataframe with all entries available from the web API, sorted by logging time. There should be one record per day. The dataframe has the following entries:\n\n* `reading_date`: a datetime object indicating the time a measurement was made\n* `level_percent`: integer percentage full\n* `level_litres`: number of lites in the tank\n\n## Scripts\n\nReporting on the current status of the tank using `kingspan-status`:\n\n``` bash\n% kingspan-status --username=test@example.com --password=s3cret\n\nHome Tank:\n Capacity = 2000\n Serial Number = 20001999\n Model = Unknown\n Level = 90% (1148 litres)\n Last Read = 2021-10-09 00:42:47.947000\n\nHistory:\n Reading date           %Full  Litres\n 30-Jan-2021 00:29      94     1224 \n 31-Jan-2021 00:59      80     1040 \n 01-Feb-2021 00:29      78     1008 \n 02-Feb-2021 00:59      76     986  \n```\n\n`kingspan-notifier` can be used to check the status of a tabk and report via email when the tank is likely to run out of oil.\n\n``` bash\n% kingspan-notifier --config kingspan.ini\nCurrent level 1148 litres\nNo notification; 196 days oil remain\n```\n\nCommand line options include:\n\n* `--config CONFIG`: a config file in ini-format\n* `--no-update`: don\'t update cache with new data (defaults to updating the DB cache)\n* `--window WINDOW`: the number of days history to consider (default: 14 days)\n* `--notice NOTICE`: the number of days before out-of-oil forecast to warn (default: 14)\n\nAn example config file is:\n\n``` ini\n[sensit]\nusername=test@example.com\npassword=s3cret\ncache=/home/me/kingspan.db\nstart-date=2021-01-31\n\n[smtp]\nserver=smtp.isp.co.uk\nusername=ispuser\nemail=test@example.com\npassword=smtps3cret\n```\n\nThe cache is an SQLite database and will be intialised if not present.\n',
    'author': 'Jon Connell',
    'author_email': 'python@figsandfudge.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/masaccio/kingspan-connect-sensor',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
