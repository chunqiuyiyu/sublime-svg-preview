"""
Sublime Text plugin to preview SVG files.
"""

import os
import shutil

# import sublime
import sublime_plugin

# pylint: disable=relative-beyond-top-level
from .utils import TMP_DIR
from .utils import run_cmd
from .utils import keep_tmp_pool
from .utils import get_origin_name
from .utils import check_cached_file
# pylint: enable=relative-beyond-top-level


class SvgPreviewCommand(sublime_plugin.TextCommand):
    """
    Called when the command is run
    """

    # pylint: disable=unused-argument
    def run(self, edit):
        """
        Convert current SVG file to PNG use Inkscape
        """

        # Firstly, we need a tmp folder to storage cache file
        if not os.path.exists(TMP_DIR):
            os.mkdir(TMP_DIR)

        # pylint: disable=attribute-defined-outside-init
        name = self.view.file_name()
        basename = os.path.basename(name)
        origin_name = get_origin_name(basename)

        cached_file_name = check_cached_file(name, basename, origin_name)

        if cached_file_name:
            tmp_png_path = os.path.join(TMP_DIR, cached_file_name)
        else:
            # In some cases, we need to get the correct object information
            # in order to convert SVG file correctly.
            query_cmd = 'inkscape --query-all "{}"'.format(name)
            result = run_cmd(query_cmd, 'Parse SVG file failed!')

            svg_id = result.split(',')[0]

            tmp_svg_path = os.path.join(TMP_DIR, basename)

            keep_tmp_pool()
            shutil.copy2(name, tmp_svg_path)

            # Convert SVG file to PNG format with Inkscape
            convert_cmd = 'inkscape --export-type=png --export-id="{}" "{}"'.format(
                svg_id, tmp_svg_path)

            run_cmd(convert_cmd, 'Convert SVG to PNG failed!')

            tmp_png_path = os.path.join(
                TMP_DIR, '{}_{}.png'.format(origin_name, svg_id))

        # Shows a popup displaying HTML content
        self.view.show_popup('<img src="file://{}">'.format(tmp_png_path))

    def is_visible(self):
        """
        Returns True if the command should be shown in the menu at this time
        """
        name = os.path.basename(self.view.file_name())
        # We only show menu when current view is in SVG file
        return name.split('.')[-1] == 'svg'
