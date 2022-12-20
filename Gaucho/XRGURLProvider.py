#!/usr/local/autopkg/python
# -*- coding: utf-8 -*-

from autopkglib import Processor, ProcessorError, URLGetter


__all__ = ["XRGURLProvider"]

# URL to consult for current version of XRG
# http://download.gauchosoft.com/xrg/latest_version.txt

update_url = "http://download.gauchosoft.com/xrg/latest_version.txt"

# Sample URL to download a specific version of XRG
# http://download.gauchosoft.com/xrg/XRG-release-1.7.3.zip


class XRGURLProvider(URLGetter):
    description = "Provides URL to the latest XRG download."
    input_variables = {
    }
    output_variables = {
        "version": {
            "description": "Version of the XRG download.",
        },
        "filename": {
            "description": "Filename of the latest XRG release download.",
        },
        "url": {
            "description": "URL to the latest XRG release download.",
        },
    }

    __doc__ = description

    def get_xrg_archive_file(self, download_version):
        """Construct the name of the XRG archive file used in
        the download URL."""
        dmg_filename = "XRG-release-{0}.zip".format(download_version)
        return dmg_filename

    def get_xrg_dmg_url(self, download_filename):
        """Construct the URL for the XRG file download."""
        # Return URL
        dmg_url = "http://download.gauchosoft.com/xrg/{0}".format(download_filename)
        return dmg_url

    def pad_version(self, download_version):
        """Pad the version number if it is shorter than expected."""
        download_version_components = download_version.split(".")
        download_version_component_count = len(download_version_components)
        if download_version_component_count < 3:
            pad_count = 3 - download_version_component_count
            padded_version = download_version + (".0" * pad_count)
        return padded_version

    def main(self):
        """Find and return a download URL."""

        # Get the string representing the requested XRG version
        download_version = self.download(update_url, text=True).strip()
        padded_version = self.pad_version(download_version)
        self.env["version"] = padded_version
        self.output("Found version %s" % self.env["version"])

        # Get the filename of the XRG disk image download using the version
        download_filename = self.get_xrg_archive_file(padded_version)
        self.env["filename"] = download_filename
        self.output("Found download filename %s" % self.env["filename"])

        # Get the URL of the XRG disk image download using the filename
        download_url = self.get_xrg_dmg_url(download_filename)

        self.env["url"] = download_url
        self.output("Found URL %s" % self.env["url"])


if __name__ == "__main__":
    processor = XRGURLProvider()
    processor.execute_shell()
