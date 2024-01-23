import shutil

import requests
import json
import logging
from pathlib import Path

from loguru import logger

logging.basicConfig(level=logging.INFO, filename='logfilename.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')



class FileDownloader:
    def __init__(self, bearer_token_pdc):
        """
        Initialize the FileDownloader with the given bearer token.

        Args:
            bearer_token_pdc (str): Bearer token for authorization.
        """
        self.token_value = bearer_token_pdc

    def download_pdf(self, url, filename):
        """
        Download a PDF from the given URL and save it to the specified filename.

        Args:
            url (str): URL of the PDF to download.
            filename (Path): Path object where the PDF should be saved.

        Returns:
            bool: True if download was successful, False otherwise.
        """
        headers = {"Authorization": self.token_value}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            pdf_info = response.json()
            pdf_url = pdf_info.get("url")
            if pdf_url:
                pdf_response = requests.get(pdf_url)
                pdf_response.raise_for_status()
                filename.write_bytes(pdf_response.content)
                return True
        except (requests.RequestException, json.JSONDecodeError) as e:
            logger.error(f"Failed to download PDF: {e}")
            return False

    def download_order_files(self, order_data, download_path=Path("./downloads")):
        """
        Download files based on the given order details.

        Args:
            order_data (dict): Order details containing links to download.
            download_path (Path): Path object indicating where to save the downloaded files.
        """
        download_path.mkdir(parents=True, exist_ok=True)

        links = order_data.get("_links", {})
        order_id = links.get("self", {}).get("href", "").split("/")[-1]

        if not order_id:
            logger.error("Skipping order due to missing '_links.self.href'")
            return
        downloaded_files = []
        # Download design files
        for i, design in enumerate(order_data.get("designs", []), start=1):
            design_folder = download_path / f'{order_id}_{i}'
            design_folder.mkdir(parents=True, exist_ok=True)
            design_url = design.get("href")
            if design_url:
                if self.download_pdf(design_url, design_folder / f"{order_id}_design_{i}.pdf"):
                    logger.info(f"Design {i} for order {order_id} downloaded to {design_folder}.")

            # Download jobsheet file inside the design folder
            jobsheet_file_url = links.get("jobsheet", {}).get("href")
            if jobsheet_file_url:
                jobsheet_folder = download_path / f'{order_id}_{i}'
                jobsheet_folder.mkdir(parents=True, exist_ok=True)
                if self.download_pdf(jobsheet_file_url, jobsheet_folder / f"{order_id}_jobsheet_{i}.pdf"):
                    logger.info(f"Jobsheet file for order {order_id} downloaded to {jobsheet_folder}.")
                downloaded_files.append(
                    (design_folder / f"{order_id}_design_{i}.pdf", jobsheet_folder / f"{order_id}_jobsheet_{i}.pdf"))


    def download_order_files_(self, order_data, download_path=Path("./downloads"), additional_download_path=Path("E:/SWITCH/PRINTCOM_PY_IN_HOLD66")):
        """
        Download files based on the given order details and copy to an additional location.

        Args:
            order_data (dict): Order details containing links to download.
            download_path (Path): Path object indicating where to save the downloaded files.
            additional_download_path (Path): Path object indicating the second location to save the downloaded files.
        """
        download_path.mkdir(parents=True, exist_ok=True)
        additional_download_path.mkdir(parents=True, exist_ok=True)  # Ensure the additional directory exists

        links = order_data.get("_links", {})
        order_id = links.get("self", {}).get("href", "").split("/")[-1]

        if not order_id:
            logger.warning("Skipping order due to missing '_links.self.href'")
            return
        downloaded_files = []
        # Download design files
        for i, design in enumerate(order_data.get("designs", []), start=1):
            design_folder = download_path / f'{order_id}_{i}'
            design_folder.mkdir(parents=True, exist_ok=True)
            additional_design_folder = additional_download_path         # / f'{order_id}_{i}'  # Additional folder path
            additional_design_folder.mkdir(parents=True, exist_ok=True)

            design_url = design.get("href")
            if design_url:
                design_file_path = design_folder / f"{order_id}_design_{i}.pdf"
                if self.download_pdf(design_url, design_file_path):
                    additional_file_path = additional_download_path / f"{order_id}_{i}_ex_1.pdf"
                    shutil.copy(design_file_path, additional_file_path)  # Copy to additional location
                    logger.info(f"Design {i} for order {order_id} downloaded to {design_folder} and copied to {additional_design_folder}.")

            # Download jobsheet file inside the design folder
            jobsheet_file_url = links.get("jobsheet", {}).get("href")
            if jobsheet_file_url:
                jobsheet_file_path = design_folder / f"{order_id}_jobsheet_{i}.pdf"
                if self.download_pdf(jobsheet_file_url, jobsheet_file_path):
                    # shutil.copy(jobsheet_file_path, additional_design_folder)  # Copy to additional location
                    logger.info(f"Jobsheet file for order {order_id} downloaded to {design_folder} and NOT copied to {additional_design_folder}.")
                downloaded_files.append((design_file_path, jobsheet_file_path))

        return downloaded_files