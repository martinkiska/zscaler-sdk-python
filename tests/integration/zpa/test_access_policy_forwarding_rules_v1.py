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

import pytest

from tests.integration.zpa.conftest import MockZPAClient
from tests.test_utils import generate_random_string


@pytest.fixture
def fs():
    yield


class TestAccessPolicyForwardingRuleV1:
    """
    Integration Tests for the Access Policy Forwarding Rules
    """

    def test_access_policy_forwarding_rules_v1(self, fs):
        client = MockZPAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        rule_id = None
        scim_group_ids = []
        network_id = None

        try:
            # Test listing SCIM groups
            idps = client.idp.list_idps()
            user_idp = next((idp for idp in idps if "USER" in idp.get("sso_type", [])), None)
            assert user_idp is not None, "No IdP with sso_type 'USER' found."

            user_idp_id = user_idp["id"]
            resp = client.scim_groups.list_groups(user_idp_id)
            assert isinstance(resp, list), "Response is not in the expected list format."
            assert len(resp) >= 2, "Less than 2 SCIM groups were found for the specified IdP."

            # Extract the first two SCIM group IDs
            scim_group_ids = [(user_idp_id, group["id"]) for group in resp[:2]]
        except Exception as exc:
            errors.append(f"Listing SCIM groups failed: {exc}")
            
        try:
            # Test listing Trusted Network Profiles
            networks = client.trusted_networks.list_networks()
            assert isinstance(networks, list), "Response is not in the expected list format."
            assert len(networks) > 0, "No Trusted Network Profile were found."
            network_id = networks[0]["network_id"]

        except Exception as exc:
            errors.append(f"Listing Trusted Network Profiles failed: {exc}")
            
        try:
            # Create a Forwarding Policy Rule
            rule_name = "tests-" + generate_random_string()
            rule_description = "updated-" + generate_random_string()
            created_rule = client.policies.add_client_forwarding_rule(
                name=rule_name,
                description=rule_description,
                action="intercept",
                conditions=[
                    ("scim_group", scim_group_ids[0][0], scim_group_ids[0][1]),
                    ("scim_group", scim_group_ids[1][0], scim_group_ids[1][1]),
                    ("trusted_network", network_id, "true"),
                ],
            )
            assert created_rule is not None, "Failed to create Forwarding Policy Rule"
            rule_id = created_rule.get("id", None)
        except Exception as exc:
            errors.append(f"Failed to create Forwarding Policy Rule: {exc}")

        try:
            # Test listing Forwarding Policy Rules
            all_timeout_rules = client.policies.list_rules("client_forwarding")
            assert any(rule["id"] == rule_id for rule in all_timeout_rules), "Forwarding Policy Rules not found in list"
        except Exception as exc:
            errors.append(f"Failed to list Forwarding Policy Rules: {exc}")

        try:
            # Test retrieving the specific Forwarding Policy Rule
            retrieved_rule = client.policies.get_rule("client_forwarding", rule_id)
            assert retrieved_rule["id"] == rule_id, "Failed to retrieve the correct Forwarding Policy Rule"
        except Exception as exc:
            errors.append(f"Failed to retrieve Forwarding Policy Rule: {exc}")

        try:
            # Update the Forwarding Policy Rule
            updated_rule_description = "Updated " + generate_random_string()
            updated_rule = client.policies.update_client_forwarding_rule(
                rule_id=rule_id,
                description=updated_rule_description,
                action="intercept",
                conditions=[
                    ("scim_group", scim_group_ids[0][0], scim_group_ids[0][1]),
                    ("scim_group", scim_group_ids[1][0], scim_group_ids[1][1]),
                ],
            )
            assert (
                updated_rule["description"] == updated_rule_description
            ), "Failed to update description for Forwarding Policy Rule"
        except Exception as exc:
            errors.append(f"Failed to update Forwarding Policy Rule: {exc}")
        
        finally:
            # Ensure cleanup is performed even if there are errors
            if rule_id:
                try:
                    client.policies.delete_rule("client_forwarding", rule_id)
                except Exception as cleanup_exc:
                    errors.append(f"Cleanup failed: {cleanup_exc}")

            # Assert that no errors occurred during the test
            assert len(errors) == 0, f"Errors occurred during the Forwarding Policy Rule operations test: {errors}"
