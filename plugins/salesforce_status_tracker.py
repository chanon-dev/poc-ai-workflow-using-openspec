"""
Salesforce Status Tracker Plugin

Tracks file upload status via TMS_Daily_Sales_File__c upsert/update.
REQ: openspec/changes/salesforce-bulk-api-dag/specs/sf-status-tracking/spec.md
"""

from __future__ import annotations

import logging
from typing import Any

import requests

logger = logging.getLogger(__name__)

API_VERSION = "v66.0"


class StatusUpdateError(Exception):
    """Raised when a status update to Salesforce fails."""


class SalesforceStatusTracker:
    """
    Tracks file upload status by upserting/updating TMS_Daily_Sales_File__c
    records via External ID (TMS_External_File_Ref__c).
    """

    def __init__(self, instance_url: str, access_token: str):
        self.instance_url = instance_url.rstrip("/")
        self.access_token = access_token
        self.base_url = (
            f"{self.instance_url}/services/data/{API_VERSION}"
            f"/sobjects/TMS_Daily_Sales_File__c/TMS_External_File_Ref__c"
        )

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def upsert_status(
        self,
        external_ref: str,
        status: str,
        **fields: Any,
    ) -> dict[str, Any]:
        """
        Upsert a TMS_Daily_Sales_File__c record via External ID.

        Creates the record if it does not exist, updates if it does.
        Does NOT use updateOnly — allows creation.

        Args:
            external_ref: External file reference ID (TMS_External_File_Ref__c value)
            status: TMS_Status__c value (e.g. "New", "Failed", "Uploading")
            **fields: Additional fields to set on the record

        Returns:
            dict with response data (id, success)
        """
        url = f"{self.base_url}/{external_ref}"

        body: dict[str, Any] = {"TMS_Status__c": status}
        body.update(fields)

        logger.info(f"Upserting status for {external_ref}: {status}")

        response = requests.patch(url, headers=self._headers(), json=body)

        if response.status_code not in (200, 201, 204):
            self._handle_error(response, external_ref, "upsert")

        result = response.json() if response.content else {}
        logger.info(
            f"Upserted {external_ref}: HTTP {response.status_code}"
        )
        return result

    def update_status(
        self,
        external_ref: str,
        status: str,
    ) -> dict[str, Any]:
        """
        Update-only a TMS_Daily_Sales_File__c record via External ID.

        Uses ?updateOnly=true to prevent accidental record creation.
        Returns 404 if record does not exist.

        Args:
            external_ref: External file reference ID
            status: TMS_Status__c value (e.g. "Uploaded", "In Progress")

        Returns:
            dict with response data

        Raises:
            StatusUpdateError: If record not found (404) or other HTTP error
        """
        url = f"{self.base_url}/{external_ref}?updateOnly=true"

        body = {"TMS_Status__c": status}

        logger.info(f"Updating status for {external_ref}: {status} (updateOnly)")

        response = requests.patch(url, headers=self._headers(), json=body)

        if response.status_code == 404:
            raise StatusUpdateError(
                f"Record not found for external ref '{external_ref}'. "
                f"Cannot update-only a non-existent record."
            )

        if response.status_code not in (200, 204):
            self._handle_error(response, external_ref, "update")

        result = response.json() if response.content else {}
        logger.info(
            f"Updated {external_ref}: HTTP {response.status_code}"
        )
        return result

    def _handle_error(
        self,
        response: requests.Response,
        external_ref: str,
        operation: str,
    ) -> None:
        """Handle HTTP error responses from Salesforce."""
        try:
            error_data = response.json()
            if isinstance(error_data, list):
                error_msg = "; ".join(
                    e.get("message", str(e)) for e in error_data
                )
            else:
                error_msg = error_data.get("message", str(error_data))
        except Exception:
            error_msg = response.text

        raise StatusUpdateError(
            f"Failed to {operation} status for '{external_ref}' "
            f"(HTTP {response.status_code}): {error_msg}"
        )
