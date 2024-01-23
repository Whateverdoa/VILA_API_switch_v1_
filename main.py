import logging

from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.responses import JSONResponse

from pathlib import Path
import json
import requests
from fastapi import FastAPI, HTTPException, Depends

from Calculations.calculations import get_today_date_str, extract_trimbox_with_pypdf2, extract_box_details
from Fastapi_print_com.pdc_conversion import process_order_item
from downloading.downloading_pdc_files import FileDownloader
from models.models_print_dot_com.models_pdc import OrderItem
from models.models_vila.models_vila import Token
from paden.pad import DOWNLOAD_PAD_VILA_TO_ESKO, DOWNLOAD_PAD, log_pad

# logging.basicConfig(level=logging.INFO,filename="printdotcom.log", format="%(asctime)s [%(levelname)s]: %(message)s")

from loguru import logger

import notifiers
from notifiers.logging import NotificationHandler

params={
    "username": 'miketenhoonte@gmail.com',
    "password": 'ttut iart mvqd amob',
    'to': 'mike@vila.nl'
}

notifier = notifiers.get_notifier("gmail")
notifier.notify(message='Vila_api_collect is running', **params)

handler = NotificationHandler("gmail", defaults=params)
logger.add(handler, level="ERROR")

logger.add(log_pad, format="{time} {level} {message}", level="INFO")

app = FastAPI()

# @app.middleware("http")
# async def token_middleware(request: Request, call_next):
#     token = request.headers.get("Authorization")
#     if not token:
#         raise HTTPException(status_code=401, detail="Token is missing")
#     request.state.token = token
#     response = await call_next(request)
#     return response


token_store = {}


def retrieve_token():
    return token_store.get('token')


@app.post("/send-token/")
async def send_token(token_data: Token):
    token_store['token'] = token_data.token
    logger.info(f"Token received {get_today_date_str()}")
    return {"message": f"Token received {get_today_date_str()}"}


@app.post("/collect_printcom_order_item")
async def collect_order_item(order_item: OrderItem, token: str = Depends(retrieve_token)):
    """
    Collects an order item and saves it to a file.
    #todo store incoming order items in a database

    """
    try:
        token = token
        # Convert to JSON
        order_item_dict = order_item.__dict__
        order_item_json = json.dumps(order_item_dict, indent=4)
        # Process the order item to remap the pdc data

        # TODO get rolwikkeling



        # dl.download_files([order_item_json])
        # print(token)
        # print(order_item_json)
        downloads = FileDownloader(token)
        # art_job_pdf_paden = downloads.download_order_files(order_data=order_item_dict,
        #                                                    download_path=DOWNLOAD_PAD)

        artjob_twice= downloads.download_order_files_(order_data=order_item_dict,
                                                      download_path=DOWNLOAD_PAD
                                                      )

        # artpdf, jobpdf = art_job_pdf_paden[0], art_job_pdf_paden[1]
        # # TODO extract data here into a new json file width height
        #
        # print(artpdf)
        # # maak een functie die de trimbox ophaalt en de width en height ophaalt
        # pdf_path2 = Path(artpdf)  # Replace with your PDF path
        # trimbox = extract_trimbox_with_pypdf2(pdf_path2)
        # trimbox_details = extract_box_details(trimbox)
        # width = trimbox_details['Width_mm']
        # height = trimbox_details['Height_mm']
        # print(width, height)
        #
        # print(jobpdf)


        # Save to file , file will be placed in a Sql database
        # remap for cerm save files
        # download files
        # zip files , delete files
        # send to cerm
        # status update printcom "ACCEPTEDBYSUPPLIER"
        # status update cerm "ACCEPTEDBYSUPPLIER"
        # status update printcom "SENTTOSUPPLIER"

        # logic to checkformat etc
        process_order_item(order_item_dict)

        file_path = Path("order_item.json")
        with file_path.open("w") as f:
            f.write(order_item_json)
            logger.info(f"Order item {order_item.order_item} collected successfully")

        return JSONResponse(content={"message": "Order item collected successfully"}, status_code=200)

    except Exception as e:
        logger.warning(f"Error: {e}")
        exception = HTTPException(status_code=500, detail=str(e))
        logger.error(f"HTTPException: {exception.detail}")
        return exception


# todo add a route to collect a list of order items for helloprint
# todo add a route to collect a list of order items for drukwerkdeal


# Schiet in naar : • http://172.27.23.70:51080/helloprint (lokaal).
# • http://92.65.9.78:61112/helloprint (web). http://92.65.9.78:61112/


# if the json is uploaded as a json body then:
@app.post("/helloprint")
async def collect_json_body(request: Request):
    data = await request.json()

    # Extract orderId and orderDetailId from the JSON data
    orderId = data['orders'][0]['orderId']
    orderDetailId = data['orders'][0]['orderLines'][0]['orderDetailId']

    # Save the JSON file with orderId and orderDetailId as the file name
    json_filename = f"{orderId}_{orderDetailId}.json"
    with open(json_filename, 'w') as json_file:
        json.dump(data, json_file)

    # Download the artwork PDF file from the URL in the 'filename' field
    pdf_url = data['orders'][0]['orderLines'][0]['filename']
    response = requests.get(pdf_url)

    # Save the PDF file with orderId and orderDetailId as the file name
    pdf_filename = f"{orderId}_{orderDetailId}.pdf"
    with open(pdf_filename, 'wb') as pdf_file:
        pdf_file.write(response.content)

    return 'JSON file collected and PDF file saved successfully!'


# if the json is uploaded as a file then:
@app.post("/helloprint/")
async def collect_json_file(file: UploadFile = File(...)):
    # Read the contents of the file
    contents = await file.read()

    # Parse the JSON data
    data = json.loads(contents)

    orderId = data['orders'][0]['orderId']
    orderDetailId = data['orders'][0]['orderLines'][0]['orderDetailId']

    # Save the JSON file with orderId and orderDetailId as the file name
    json_filename = f"{orderId}_{orderDetailId}.json"
    with open(json_filename, 'w') as json_file:
        json.dump(data, json_file)

    # Download the PDF file from the URL in the 'filename' field
    pdf_url = data['orders'][0]['orderLines'][0]['filename']
    response = requests.get(pdf_url)

    # Save the PDF file with orderId and orderDetailId as the file name
    pdf_filename = f"{orderId}_{orderDetailId}.pdf"
    with open(pdf_filename, 'wb') as pdf_file:
        pdf_file.write(response.content)

    return {"message": "JSON as a file collected and PDF file saved successfully!"}

# uvicorn main:app --host 92.65.9.78 --port 61112
