# plugins/salesforce_bulk_loader.py

import requests
import time
import os
import gzip
from concurrent.futures import ThreadPoolExecutor, as_completed

class SalesforceBulkLoader:
    """
    Wrapper for Salesforce Bulk API 2.0 Ingest.
    Supports GZIP compression and parallel uploads.
    """
    
    def __init__(self, instance_url: str, access_token: str):
        self.base_url = f"{instance_url}/services/data/v59.0/jobs/ingest"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def load_files_parallel(self, object_name: str, csv_files: list, external_id: str = None, max_workers: int = 5) -> list:
        """
        Parallel upload wrapper.
        For Bulk API 2.0, we typically create one job per file or batch of files (if combining).
        Here we assume 1 file = 1 job for simplicity of restartability.
        """
        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self._process_single_file, object_name, f, external_id): f 
                for f in csv_files
            }
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({"file": futures[future], "error": str(e), "status": "Failed"})
                    
        return results

    def _process_single_file(self, object_name: str, file_path: str, external_id: str) -> dict:
        """
        Execute full lifecycle for one CSV file: Create Job -> Upload -> Close -> Wait
        """
        # 1. Create Job
        operation = "upsert" if external_id else "insert"
        payload = {
            "object": object_name,
            "contentType": "CSV",
            "operation": operation,
            "lineEnding": "LF"
        }
        if external_id:
            payload["externalIdFieldName"] = external_id
            
        job_resp = requests.post(self.base_url, headers=self.headers, json=payload)
        job_resp.raise_for_status()
        job_id = job_resp.json()["id"]
        
        try:
            # 2. Upload Data (GZIP)
            with open(file_path, "rb") as f:
                # If file is not already gzipped, we might want to gzip it on the fly
                # But spec says stage is already gzipped. If not, we can read/compress here.
                # Assuming input is raw CSV here based on dag_factory logic (to_csv)
                # Let's compress it for upload
                compressed_data = gzip.compress(f.read())
                
            upload_headers = self.headers.copy()
            upload_headers["Content-Type"] = "text/csv"
            upload_headers["Content-Encoding"] = "gzip"
            
            requests.put(f"{self.base_url}/{job_id}/batches", headers=upload_headers, data=compressed_data).raise_for_status()
            
            # 3. Close Job (Start Processing)
            state_payload = {"state": "UploadComplete"}
            requests.patch(f"{self.base_url}/{job_id}", headers=self.headers, json=state_payload).raise_for_status()
            
            # 4. Poll for Completion
            return self._poll_job(job_id)
            
        except Exception as e:
            # Attempt to abort if failed
            requests.patch(f"{self.base_url}/{job_id}", headers=self.headers, json={"state": "Aborted"})
            raise e

    def _poll_job(self, job_id: str) -> dict:
        """Poll job status until complete"""
        while True:
            resp = requests.get(f"{self.base_url}/{job_id}", headers=self.headers)
            info = resp.json()
            state = info["state"]
            
            if state in ["JobComplete", "Failed", "Aborted"]:
                return {
                    "job_id": job_id,
                    "state": state,
                    "records_processed": info.get("numberRecordsProcessed", 0),
                    "records_failed": info.get("numberRecordsFailed", 0)
                }
            
            time.sleep(5)
