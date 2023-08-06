"""
mblog: a minimal markdown blog
"""
from __future__ import print_function

# pylint: disable=W
# pylint: disable=missing-docstring
try:

    import sys

    from mblog.config import HOST, PORT, DEBUG, USER, DATABASE_NEEDS_FTS
    from mblog.config import app, database
    from mblog.models import Entry

    if DATABASE_NEEDS_FTS:
        from mblog.models import FTSEntry
    from mblog.routes import *

except ImportError as importError:
    print("All dependencies aren't installed. \n Error: {} \n Run: $ pip install -r requirements.txt".format(
        str(importError)), file=sys.stderr)
    exit(1)


def startBlog():
    database.create_tables([Entry], safe=True)
    if DATABASE_NEEDS_FTS:
        database.create_tables([FTSEntry], safe=True)
    app.run(debug=DEBUG, host=HOST, port=PORT)
