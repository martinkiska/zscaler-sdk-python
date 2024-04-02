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
from tests.integration.zia.conftest import MockZIAClient
from tests.test_utils import generate_random_string

@pytest.fixture
def fs():
    yield


class TestRuleLabels:
    """
    Integration Tests for the Rule Label
    """

    @pytest.mark.asyncio
    async def test_rule_labels(self, fs):
        client = MockZIAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        label_name = "tests-" + generate_random_string()
        label_description = "tests-" + generate_random_string()

        try:
            # Create a new rule label
            created_label = client.labels.add_label(
                name=label_name,
                description=label_description,
            )
            assert created_label is not None
            assert created_label.name == label_name
            assert created_label.description == label_description

            label_id = created_label.id
        except Exception as exc:
            errors.append(exc)

        try:
            # Retrieve the created rule label by ID
            retrieved_label = client.labels.get_label(label_id)
            assert retrieved_label.id == label_id
            assert retrieved_label.name == label_name
        except Exception as exc:
            errors.append(exc)

        try:
            # Update the rule label
            updated_name = label_name + " Updated"
            client.labels.update_label(label_id, name=updated_name)

            updated_label = client.labels.get_label(label_id)
            assert updated_label.name == updated_name
        except Exception as exc:
            errors.append(exc)

        try:
            # List rule labels and ensure the updated label is in the list
            labels_list = client.labels.list_labels()
            assert any(label.id == label_id for label in labels_list)
        except Exception as exc:
            errors.append(exc)

        try:
            # Search for the rule label by name
            search_result = client.labels.get_label_by_name(
                updated_name
            )
            assert search_result is not None
            assert search_result.id == label_id
        except Exception as exc:
            errors.append(exc)

        try:
            # Delete the rule label
            delete_response_code = client.labels.delete_label(label_id)
            assert str(delete_response_code) == "204"
        except Exception as exc:
            errors.append(exc)

        # Assert that no errors occurred during the test
        assert (
            len(errors) == 0
        ), f"Errors occurred during the rule label lifecycle test: {errors}"
