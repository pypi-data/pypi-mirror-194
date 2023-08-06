# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mediasorter']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'aiohttp>=3.8.3,<4.0.0',
 'async-cache>=1.1.1,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'rich>=13.1.0,<14.0.0']

entry_points = \
{'console_scripts': ['mediasorter = mediasorter.cli:main']}

setup_kwargs = {
    'name': 'multimediasorter',
    'version': '1.0.11',
    'description': '',
    'long_description': '# (multi)mediasorter\n\nmediasorter is a tool to automatically "sort" media files from a source naming format\ninto something nicer for humans to read/organize, and for tools like Jellyfin to parse\nand collect metadata for. It uses The Movie DB for movie metadata and TVMaze for\nTV metadata to obtain additional information, then performs the "sort" via\na user-selectable mechanism. In this aspect it seeks to be a replacement for\nFileBot and other similar tools.\n\nMost aspects of mediasorter can be configured, either inside the main configuration file,\nor via command-line arguments; it hopes to remain simple yet flexible, doing exactly\nwhat the administrator wants and nothing more.\n\nmediasorter is free software, released under the GNU GPL version 3 (or later).\nCore of the mediasorter is written in Python 3 using asyncio and a simple CLI script and makes use of Click (`python3-click`) and YAML (`python3-yaml`).\n\n## Usage\n\n1. Install on your machine or in a virtualenv.\n\n``` bash\n$ pip install multimediasorter  # install\n```\n\n``` bash\n# Install the bundled config.yaml that should include all that is needed,\n# (!) except for the TMDB api key.\n$ mediasorter --setup\n```\n\n2. Edit the configuration file with your TMDB API key (otherwise only TV shows searches will work).\n3. Run `mediasorter.py --help` for detailed help.\n\n```bash\n# Or e.g.:\n$ mediasorter tests/test_data/ -dtv ~/Media/Series -dmov ~/Media/Movies\n```\n4. Profit!\n\n## Metainfo Tagging\n\nWith the `-tm`/`--tag-metainfo` option, additional info can be added to the destination filename to leverage Jellyfin\'s ["multiple movie versions"](https://jellyfin.org/docs/general/server/media/movies.html#multiple-versions-of-a-movie) feature. Currently, this only works with Movies (not TV episodes) in Jellyfin, and thus in mediasorter as well.\n\nWhen this option is specified, the information found in the `metainfo_map` in the configuration file which is present in the source filename will be appended, using the square-brackets format, to the end of the destination filename.\n\nWhen parsing, the list is iterated through in the order specified, and then for each item, the source filename is searched for the relevant regex match. If found, the value will be appended (once) to the metainfo string. The entries are grouped by type, for example cuts/editions first, then resolutions, then media types, etc. to produce a coherent and consistent string.\n\nA large sample of possible match values is included in the `mediasorter.yml.sample` file, but more can be added or some removed as desired.\n\nAs an example, the following might be a destination filename with metainfo tagging using the default map:\n\n```\nLord of the Rings: The Return of the King, The (2003) - [Extended Edition 2160p BD Remux 7.x Atmos TrueHD].mkv\n```\n\n## Replacement\n\nBy default, `mediasorter` will replace an existing destination file, if one exists,\nwith a new one during a run. This is useful if new media comes in which should\nreplace the existing media (e.g. an upgraded quality version). To disable this\nbehaviour, use `--no-upgrade`.\n\nThis behaviour is redundant when meta-info tagging is enabled for Movies, since the\ndifferentiating quality profile would trigger a new file to be created anyway; it is\nthus mostly useful for TV which does not support this feature.\n\n## Search Overrides\n\nSometimes, the name of a piece of media, as extracted from the file, will not return\nproper results from the upstream metadata providers. If this happens, `mediasorter`\nincludes an option in the configuration file to specify search overrides.\nFor example, the TV show "S.W.A.T." does not return sensible results, so it\ncan be overridden like so:\n\n``` yaml\ntv:\n  search_overrides:\n    "s w a t": "swat"\n    # ...\n```\n\nThis is currently the only *provided* example for demonstration purposes,\nbut it can happen to many titles. If you find a title that returns\nno results consider adding it to this list on your local system.\n\n## Name Overrides\n\nSometimes, the name returned by the metadata providers might not\nmatch what you want to sort as. Thus `mediasorter` can override\ntitles based on a list provided in the configuration file. For example,\nif you want the TV show "Star Trek" to be named\n"Star Trek: The Original Series" instead, it can be overridden like so:\n\n``` yaml\ntv:\n  name_overrides:\n    "Star Trek": "Star Trek: The Original Series"\n    # ...\n```\n\nThese overrides are specific to media type (`tv` or `movie`) to avoid conflicts,\ne.g. in this example, with the 2009 film "Star Trek" which would also be changed\n(erroneously) if this were global.\n\nName overrides are handled *before* adjusting a suffixed "The", so entries containing\n"The" should be written normally, e.g. "The Series" instead of "Series, The"\neven if the latter is what is ultimately written.\n\n## Scan multiple directories\n\n`mediasorter` can be asked to scan multiple directories. Either via CLI or via\nthe configuration file - especially handy when running `mediasorter` as a cron job.\n```yaml\n# Use this to configure what directories should be sorted instead of the CLI argument(s).\nscan_sources:\n\n  - src_path: ~/Downloads-01\n    media_type: auto  # force only a specific media type tv/movie/auto\n    tv_shows_output: ~/Media/TV  # where to put recognized TV shows\n    movies_output: ~/Media/Movies\n\n  - src_path: ~/Downloads-02\n    media_type: auto\n    tv_shows_output: ~/Media/TV\n    movies_output: ~/Media/Movies\n```\n\n```bash\n# Crontab\n$ * * * * * mediasorter -a move\n```\n\n## fix-episodes.sh\n\nmediasorter isn\'t that smart. For instance, if a show has inconsistent episode numbers between, say, airdate and a DVD, it can give episodes the wrong numbering.\n\nFixing this manually is quite cumbersome, and after having to deal with it more than once, I created this quick-and-dirty script that will quickly rename such files, especially for ranges of episodes that are incorrectly numbered.\n\nRun it with no arguments for usage information.\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
