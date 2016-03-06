# -*- coding: utf-8 -*-

"""
DBB Ranking Parser
~~~~~~~~~~~~~~~~~~

Extract league rankings from the DBB (Deutscher Basketball Bund e.V.)
website.

The resulting data is structured as a list of dictionaries.

:Copyright: 2006-2016 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from .conversion import convert_attributes
from .document import get_rank_values, has_team_withdrawn, select_rank_rows
from .http import fetch_content


def load_ranking(url):
    """Fetch the URL's content and yield ranks extracted from it."""
    html = fetch_content(url)
    return parse(html)


def parse(html):
    """Yield ranks extracted from HTML document."""
    trs = select_rank_rows(html)
    return _parse_rank_rows(trs)


def _parse_rank_rows(trs):
    """Yield ranks extracted from table rows."""
    for tr in trs:
        rank = _parse_rank_row(tr)
        if rank:
            yield rank


def _parse_rank_row(tr):
    """Attempt to extract a single rank's properties from a table row."""
    team_has_withdrawn = has_team_withdrawn(tr)

    values = get_rank_values(tr, team_has_withdrawn)

    if not values:
        return None

    attributes = convert_attributes(values)
    attributes['withdrawn'] = team_has_withdrawn
    return attributes
