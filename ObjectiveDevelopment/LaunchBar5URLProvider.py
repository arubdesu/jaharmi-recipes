#!/usr/local/autopkg/python
# -*- coding: utf-8 -*-
#
# Copyright 2013 Jeremy Reichman <jaharmi@jaharmi.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from collections import defaultdict
import os
from autopkglib import Processor, ProcessorError, URLGetter

try:
    from plistlib import loads as readPlistFromString  # Python 3
except ImportError:
    from plistlib import readPlistFromString  # Python 2

__all__ = ["LaunchBar5URLProvider"]

# URL to consult for current version of LaunchBar
# https://sw-update.obdev.at/update-feeds/launchbar-5.plist
update_url = "https://sw-update.obdev.at/update-feeds/launchbar-5.plist"


class LaunchBar5URLProvider(URLGetter):
    description = "Provides URL to the latest LaunchBar 5 download."
    input_variables = {
    }
    output_variables = {
        "version": {
            "description": "Version of the LaunchBar download.",
        },
        "filename": {
            "description": "Filename of the latest LaunchBar release download.",
        },
        "url": {
            "description": "URL to the latest LaunchBar release download.",
        },
    }

    __doc__ = description

    def get_update_feed_data(self, update_url):
        """Find the latest version of LaunchBar and output as a string."""
        try:
            html = self.download(update_url)
            plist_data = readPlistFromString(html)
        except BaseException as e:
            raise ProcessorError("Can't download %s: %s" % (update_url, e))
        return plist_data

    def get_release_data(self, plist_data, sw_release="stable"):
        """Get the update data for the specific LaunchBar release."""
        dicts_by_name = defaultdict(list)
        for a in plist_data:
            dicts_by_name[a['ReleaseLifecycle']] = a
        update_release_data = dicts_by_name[sw_release]
        return update_release_data

    def get_download_url(self, sw_release_data):
        """Get the download URL from the LaunchBar release update data."""
        # Return URL
        dmg_url = sw_release_data['DownloadURL']
        return dmg_url

    def get_download_version(self, sw_release_data):
        """Get the version of the LaunchBar download from the release update data."""
        dmg_version = sw_release_data['BundleShortVersionString']
        return dmg_version

    def main(self):
        """Find and return a download URL."""

        # Get update feed data
        update_feed_data = self.get_update_feed_data(update_url)
        self.output("Fetching update feed data from URL %s" % update_url)
        update_release_data = self.get_release_data(update_feed_data, 'stable')
        if update_release_data:
            self.output("Found update feed data.")

        # Get the URL of the LaunchBar disk image download using the filename
        download_url = self.get_download_url(update_release_data)
        self.env["url"] = download_url
        self.output("Found URL %s" % self.env["url"])

        # Get the string representing the requested LaunchBar version
        download_version = self.get_download_version(update_release_data)
        self.env["version"] = download_version
        self.output("Found version %s" % self.env["version"])

        # Get the filename of the disk image for the requested LaunchBar version
        download_filename = download_url.split('/')[-1]
        self.env["filename"] = download_filename
        self.output("Found download filename %s" % self.env["filename"])


if __name__ == "__main__":
    processor = LaunchBar5URLProvider()
    processor.execute_shell()
