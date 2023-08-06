# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deutschland',
 'deutschland.autobahn',
 'deutschland.autobahn.api',
 'deutschland.autobahn.apis',
 'deutschland.autobahn.model',
 'deutschland.autobahn.models',
 'deutschland.bundesanzeiger',
 'deutschland.bundesnetzagentur',
 'deutschland.handelsregister',
 'deutschland.lebensmittelwarnung',
 'deutschland.presseportal',
 'deutschland.verena']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.3.1,<9.0.0',
 'Shapely>=1.7.1,<2.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'boto3>=1.18.9,<2.0.0',
 'dateparser>=1.0.0,<2.0.0',
 'gql>=2.0.0,<3.0.0',
 'lxml>=4.6.3,<5.0.0',
 'mapbox-vector-tile>=1.2.1,<2.0.0',
 'pypresseportal>=0.1,<0.2',
 'requests>=2.26.0,<3.0.0',
 'slugify>=0.0.1,<0.0.2',
 'tensorflow>=2.5.0,<3.0.0']

setup_kwargs = {
    'name': 'deutschland',
    'version': '0.1.8',
    'description': '',
    'long_description': '[![PyPI version deutschland](https://badge.fury.io/py/deutschland.svg)](https://pypi.python.org/pypi/deutschland/)\n[![GitHub license](https://img.shields.io/github/license/bundesAPI/deutschland.svg)](https://github.com/bundesAPI/deutschland/blob/main/LICENSE)\n\n[![Lint](https://github.com/bundesAPI/deutschland/actions/workflows/black.yml/badge.svg?branch=main)](https://github.com/bundesAPI/deutschland/actions/workflows/black.yml)\n[![Publish Python 🐍 distributions 📦 to PyPI and TestPyPI](https://github.com/bundesAPI/deutschland/actions/workflows/publish.yml/badge.svg?branch=main)](https://github.com/bundesAPI/deutschland/actions/workflows/publish.yml)\n[![Run Python 🐍 tests](https://github.com/bundesAPI/deutschland/actions/workflows/runtests.yml/badge.svg?branch=main)](https://github.com/bundesAPI/deutschland/actions/workflows/runtests.yml)\n\n# Deutschland\nA python package that gives you easy access to the most valuable datasets of Germany.\n\n## Installation\n```bash\npip install deutschland\n```\n\n## Geographic data\nFetch information about streets, house numbers, building outlines, …\n\n```python\nfrom deutschland import Geo\ngeo = Geo()\n# top_right and bottom_left coordinates\ndata = geo.fetch([52.50876180448243, 13.359631043007212], \n                 [52.530116236589244, 13.426532801586827])\nprint(data.keys())\n# dict_keys([\'Adresse\', \'Barrierenlinie\', \'Bauwerksflaeche\', \'Bauwerkslinie\', \'Bauwerkspunkt\', \'Besondere_Flaeche\', \'Besondere_Linie\', \'Besonderer_Punkt\', \'Gebaeudeflaeche\', \'Gebaeudepunkt\', \'Gewaesserflaeche\', \'Gewaesserlinie\', \'Grenze_Linie\', \'Historischer_Punkt\', \'Siedlungsflaeche\', \'Vegetationslinie\', \'Verkehrsflaeche\', \'Verkehrslinie\', \'Verkehrspunkt\', \'Hintergrund\'])\n\nprint(data["Adresse"][0])\n# {\'geometry\': {\'type\': \'Point\', \'coordinates\': (13.422642946243286, 52.51500157651358)}, \'properties\': {\'postleitzahl\': \'10179\', \'ort\': \'Berlin\', \'ortsteil\': \'Mitte\', \'strasse\': \'Holzmarktstraße\', \'hausnummer\': \'55\'}, \'id\': 0, \'type\': \'Feature\'}\n```\n\n\n\n\n## Company Data\n\n### Bundesanzeiger\nGet financial reports for all german companies that are reporting to Bundesanzeiger.\n\n```python\nfrom deutschland import Bundesanzeiger\nba = Bundesanzeiger()\n# search term\ndata = ba.get_reports("Deutsche Bahn AG")\n# returns a dictionary with all reports found as fulltext reports\nprint(data.keys())\n# dict_keys([\'Jahresabschluss zum Geschäftsjahr vom 01.01.2020 bis zum 31.12.2020\', \'Konzernabschluss zum Geschäftsjahr vom 01.01.2020 bis zum 31.12.2020\\nErgänzung der Veröffentlichung vom 04.06.2021\',\n```\n*Big thanks to Nico Duldhardt and Friedrich Schöne, who [supported this implementation with their machine learning model](https://av.tib.eu/media/52366).*\n\n### Handelsregister\nFetch general company information about any company in the Handelsregister.\n\n```python\nfrom deutschland import Handelsregister\nhr = Handelsregister()\n# search by keywords, see documentation for all available params\nhr.search(keywords="Deutsche Bahn Aktiengesellschaft")\nprint(hr)\n```\n\n\n## Consumer Protection Data\n\n### Lebensmittelwarnung\nGet current product warnings provided by the german federal portal lebensmittelwarnung.de. \n\n```python\nfrom deutschland import Lebensmittelwarnung\nlw = Lebensmittelwarnung()\n# search by content type and region, see documetation for all available params\ndata = lw.get("lebensmittel", "berlin")\nprint(data)\n# [{\'id\': 19601, \'guid\': \'https://www.lebensmittelwarnung.de/bvl-lmw-de/detail/lebensmittel/19601\', \'pubDate\': \'Fri, 10 Feb 2017 12:28:45 +0000\', \'imgSrc\': \'https://www.lebensmittelwarnung.de/bvl-lmw-de/opensaga/attachment/979f8cd3-969e-4a6c-9a8e-4bdd61586cd4/data.jpg\', \'title\': \'Sidroga Bio Säuglings- und Kindertee\', \'manufacturer\': \'Lebensmittel\', \'warning\': \'Pyrrolizidinalkaloide\', \'affectedStates\': [\'Baden-Württemberg\', \'...\']}]\n```\n\n## Federal Job Openings\n\n### NRW\n\n#### VERENA\nGet open substitute teaching positions in NRW from https://www.schulministerium.nrw.de/BiPo/Verena/angebote\n```python\nfrom deutschland import Verena\nv = Verena()\ndata = v.get()\nprint(data)\n# a full example data can be found at deutschland/verena/example.md\n# [{ "school_id": "99999", "desc": "Eine Schule\\nSchule der Sekundarstufe II\\ndes Landkreis Schuling\\n9999 Schulingen", "replacement_job_title": "Lehrkraft", "subjects": [ "Fach 1", "Fach 2" ], "comments": "Bemerkung zur Stelle: Testbemerkung", "duration": "01.01.2021 - 01.01.2022", ...} ...]\n\n\n## Autobahn\n\nGet data from the Autobahn.\n\n```python\nfrom deutschland import autobahn\nfrom deutschland.autobahn.api import default_api\n\nfrom pprint import pprint\n\nautobahn_api_instance = default_api.DefaultApi()\n\ntry:\n    # Auflistung aller Autobahnen\n    api_response = autobahn_api_instance.list_autobahnen()\n    pprint(api_response)\n\n    # Details zu einer Ladestation\n    station_id = "RUxFQ1RSSUNfQ0hBUkdJTkdfU1RBVElPTl9fMTczMzM="  # str |\n    api_response = autobahn_api_instance.get_charging_station(station_id)\n    pprint(api_response)\n\nexcept autobahn.ApiException as e:\n    print("Exception when calling DefaultApi->get_charging_station: %s\\n" % e)\n```\n\n\n## Presseportal\n\nFor further information see: https://github.com/tcmetzger/pypresseportal\n\n```python\nfrom deutschland.presseportal import PresseportalApi\n\npresseportal = PresseportalApi("YOUR_KEY_HERE")\n\nstories = presseportal.get_stories()    \n```\n',
    'author': 'Lilith Wittmann',
    'author_email': 'mail@lilithwittmann.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bundesAPI/deutschland',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
