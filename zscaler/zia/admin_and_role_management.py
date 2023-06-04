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
from restfly.endpoint import APIEndpoint

from zscaler.utils import Iterator, snake_to_camel


class AdminRoleManagementAPI(APIEndpoint):
    def list_roles(self, **kwargs) -> BoxList:
        """
        Return a list of the configured admin roles in ZIA.

        Args:
            **kwargs: Optional keyword args.

        Keyword Args:
            include_auditor_role (bool): Set to ``True`` to include auditor role information in the response.
            include_partner_role (bool): Set to ``True`` to include partner admin role information in the response.

        Returns:
            :obj:`BoxList`: A list of admin role resource records.

        Examples:
            Get a list of all configured admin roles:
            >>> roles = zia.admin_and_management_roles.list_roles()

        """
        payload = {snake_to_camel(key): value for key, value in kwargs.items()}

        return self._get("adminRoles/lite", params=payload)
