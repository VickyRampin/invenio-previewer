# -*- coding: utf-8 -*-

"""GIS data previewer"""

from __future__ import absolute_import, print_function
from flask import render_template
from ..proxies import current_previewer

import zipfile
import cchardet as chardet
from six import binary_type

previewable_extensions = ['zip']

def can_preview(file):
    """Check if file can be previewed"""
    return file.is_local() and file.has_extensions('.zip')
    # return true if SHP, SHX, and DBF present
    with file.open() as fp:
        zf = zipfile.ZipFile(fp)
        # Detect filenames encoding.
        sample = ' '.join(zf.namelist())
        if not isinstance(sample, binary_type):
            sample = sample.encode('utf-16be')
        encoding = chardet.detect(sample).get('encoding', 'utf-8')
        for i, info in enumerate(zf.infolist()):
            if i.endswith('.shp') or i.endswith('.dbf') or i.endswith('.shx'):
                continue
            else:
                continue

def preview(file):
    """Preview file."""
    return render_template(
        'invenio_previewer/gis.html',
        file=file,
        js_bundles=current_previewer.js_bundles + ['gis_js.js'],
        css_bundles=current_previewer.css_bundles + ["gis_css.css"]
    )
