# -*- coding: utf-8 -*-

# Copyright (c) 2023, Zscaler Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


from box import Box, BoxList
from requests import Response

from zscaler.zpa.client import ZPAClient


class IsolationProfileAPI:
    def __init__(self, client: ZPAClient):
        self.rest = client

    def list_profiles(self, **kwargs) -> BoxList:
        """
        Returns a list of all configured isolation profiles.

        Keyword Args:
            **max_items (int):
                The maximum number of items to request before stopping iteration.
            **max_pages (int):
                The maximum number of pages to request before stopping iteration.
            **pagesize (int):
                Specifies the page size. The default size is 20, but the maximum size is 500.
            **search (str, optional):
                The search string used to match against features and fields.

        Returns:
            :obj:`list`: A list of all configured isolation profiles.

        Examples:
            >>> for isolation_profiles in zpa.isolation_profiles.list_profiles():
            ...    pprint(isolation_profiles)

        """
        list, _ = self.rest.get_paginated_data(path="/isolation/profiles", data_key_name="list", **kwargs)
        return list

    def get_profile_by_name(self, name):
        """
        Returns information on the specified isolation profile by name.
        """
        profiles = self.list_profiles()
        for profile in profiles:
            if profile.get("name") == name:
                return profile
        return None

    def get_profile_by_id(self, profile_id):
        """
        Returns information on the specified isolation profile by ID.
        """
        profiles = self.list_profiles()
        for profile in profiles:
            # Ensure both IDs are compared as strings
            if str(profile.get("id")) == str(profile_id):
                return profile
        return None
