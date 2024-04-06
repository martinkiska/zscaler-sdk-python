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


class TestURLCategories:
    """
    Integration Tests for the URL Categories
    """

    @pytest.mark.asyncio
    async def test_url_categories(self, fs):
        client = MockZIAClient(fs)
        errors = []  # Initialize an empty list to collect errors

        category_name = "tests-" + generate_random_string()
        category_description = "tests-" + generate_random_string()
        category_id = None

        try:
            # Attempt to create a new URL category
            created_category = client.url_categories.add_url_category(
                configured_name=category_name,
                description=category_description,
                super_category="USER_DEFINED",
                keywords=["microsoft"],
                custom_category=True,
                db_categorized_urls=[".creditkarma.com", ".youku.com"],
                type="URL_CATEGORY",
                urls=[".coupons.com"],
                ip_ranges=["3.217.228.0/25", "3.235.112.0/24"],
                ip_ranges_retaining_parent_category=["13.107.6.152/31"],
            )
            category_id = (
                created_category.id
            )  # Assuming this does not throw an exception
            assert created_category is not None, "URL Category creation returned None"
            assert (
                created_category.configured_name == category_name
            ), "Category name mismatch"
            assert (
                created_category.description == category_description
            ), "Category description mismatch"
        except Exception as exc:
            errors.append(f"Failed to add URL category: {exc}")

        try:
            # Attempt to retrieve the created URL category by ID
            retrieved_category = client.url_categories.get_category(category_id)
            assert (
                retrieved_category.id == category_id
            ), "Retrieved category ID mismatch"
            assert (
                retrieved_category.configured_name == category_name
            ), "Retrieved category name mismatch"
        except Exception as exc:
            errors.append(f"Failed to retrieve URL category: {exc}")

        try:
            # Attempt to update the URL category
            updated_name = category_name + " Updated"
            client.url_categories.update_url_category(
                category_id, configured_name=updated_name
            )
            updated_category = client.url_categories.get_category(category_id)
            assert (
                updated_category.configured_name == updated_name
            ), "Failed to update category name"
        except Exception as exc:
            errors.append(f"Failed to update URL category: {exc}")

        try:
            # Attempt to list URL categories and check if the updated category is in the list
            category_list = client.url_categories.list_categories()
            assert any(
                category.id == category_id for category in category_list
            ), "Updated category not found in list"
        except Exception as exc:
            errors.append(f"Failed to list URL categories: {exc}")

        try:
            # Attempt to search for the URL category by name
            search_result = client.url_categories.get_category_by_name(updated_name)
            assert search_result is not None, "Search returned None"
            assert search_result.id == category_id, "Search result ID mismatch"
        except Exception as exc:
            errors.append(f"Failed to search URL category by name: {exc}")

        finally:
            # Cleanup: Attempt to delete the URL category
            if category_id:
                try:
                    delete_response_code = client.url_categories.delete_category(
                        category_id
                    )
                    assert delete_response_code == 204, "Failed to delete category"
                except Exception as exc:
                    errors.append(f"Cleanup failed: {exc}")

        # Assert that no errors occurred during the test
        assert (
            len(errors) == 0
        ), f"Errors occurred during the URL category lifecycle test: {errors}"
