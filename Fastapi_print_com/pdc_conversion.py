import unicodedata
from dataclasses import asdict
from pathlib import Path
from typing import List, Dict, Any
import logging
import json

from Calculations.calculations import calculate_dimensions_with_winding
from paden.pad import DOWNLOAD_PAD, DOWNLOAD_PAD_VILA_TO_ESKO, testzip
from models.models_esko.esko_models import OrderInfo, Delivery, Contact
from models.models_print_dot_com.models_pdc import OrderItem, Shipment, Address, Options
import shutil

# Initialize logging

logging.basicConfig(level=logging.INFO,filename="printdotcom.log", format="%(asctime)s [%(levelname)s]: %(message)s")


def zip_folder(src_folder: Path, dest_zip: Path):
    """
    Zips a folder.

    Args:
        src_folder (Path): The path to the source folder you want to zip.
        dest_zip (Path): The path to the destination zip file.

    Returns:
        Path: The path to the created zip file.
    """
    shutil.make_archive(dest_zip, 'zip', src_folder)
    return dest_zip.with_suffix('.zip')


def verwijder_speciale_tekens(input_string: str) -> str:
    """
    Removes special characters and diacritic marks from the input string
    by normalizing the unicode characters and replacing certain non-ASCII characters.

    Args:
        input_string (str): The string from which special characters need to be removed.

    Returns:
        str: The string with special characters and diacritic marks removed.
    """
    # Mapping of non-ASCII characters to their closest ASCII equivalents
    char_mapping = {
        'ø': 'o',
        'å': 'a',
        'Ø': 'O',
        'Å': 'A',
        '/': ' ',
        '.': '',
        # Add more mappings as needed
    }

    # Normalize the string and remove diacritic marks
    normalized_string = unicodedata.normalize('NFKD', input_string)
    no_diacritics = "".join([c for c in normalized_string if not unicodedata.combining(c)])

    # Replace non-ASCII characters using the mapping
    result = "".join([char_mapping.get(c, c) for c in no_diacritics])
    return result


def extract_design_info(data: dict):
    """
    Extract information for each design.

    Args:
        data (dict): The order data.

    Returns:
        list[dict]: A list of dictionaries containing the extracted information for each design.
    """
    designs_info = []

    designs = data.get("designs", [])
    for design in designs:
        design_info_ = {
            "id": design.get("id"),
            "copies": design.get("copies"),
            "href": design.get("href"),
        }
        designs_info.append(design_info_)

    return designs_info


def load_json(filepath: Path) -> Dict[str, Any]:
    """Load JSON file and return its contents
        as Python dictionary.

    Args:
        filepath (Path): The path to the JSON file.

    Returns:
        Dict[str, Any]: The contents of the JSON file as dictionary.
    """
    with filepath.open("r") as f:
        return json.load(f)


def save_json(data: Dict[str, Any], filepath: Path) -> None:
    """Save  Python dictionary as JSON file.

    Args:
        data (Dict[str, Any]): The data to save.
        filepath (Path): The path to the JSON file to save.
        
     # Create the directory if it doesn't exist"""
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with filepath.open("w") as f:
        json.dump(data, f, indent=4)


def convert_address_to_contact(address: Address) -> Contact:
    """Converts an Address object to dataclass Contact object.

    Args:
        address (Address): The Address object to convert.

    Returns:
        Contact: The converted Contact object.
    """
    return Contact(
        LastName=verwijder_speciale_tekens(address.lastName),
        FirstName=verwijder_speciale_tekens(address.firstName),
        # Initials=address.firstName[0],
        Initials='',
        Title='Mr./Mevr.',
        PhoneNumber=address.telephone,
        FaxNumber='',
        GSMNumber='',
        Email=address.email,
        Function=''
    )


def convert_shipment_to_delivery(shipment: Shipment) -> Delivery:
    """Converts Shipment object to Delivery object.

    Args:
        shipment (Shipment): The Shipment object to convert.

    Returns:
        Delivery: The converted Delivery object.
    """
    return Delivery(
        Type=shipment.method,
        Comment='',
        AddressId=str(shipment.addressId),
        ExpectedDate=shipment.deliveryDate
    )


def convert_order_item_to_order_info(order_item: OrderItem) -> List[OrderInfo]:
    """Converts an OrderItem object to a list of OrderInfo objects.

    Args:
        order_item (OrderItem): The OrderItem object to convert.

    Returns:
        List[OrderInfo]: A list of converted OrderInfo objects.
    """
    all_order_info = []
    shipments = order_item.shipments
    contacts = order_item.shipments[0]['address']
    from_pdc_in_address = Address(**contacts)
    contact_from_first_shipment = convert_address_to_contact(from_pdc_in_address)

    options = order_item.options
    # Set default values for missing keys
    options.setdefault('output_direction', 'outer_0')
    options.setdefault('shape', 'custom_shape')



    def price_per_1000(totalprice, quantity):
        if quantity == 0:
            return 0
        else:
            return round((totalprice / quantity) * 1000, 2)

    # Additional logic for recalculations can be added here.

    def check_for_white(colors):
        """Check if the color white exists in the given list of colors.

        Args:
            colors (List[str]): List of color names.

        Returns:
            str: 'Y' if white exists, otherwise 'N'.
        """
        for color in colors:
            if "white" in color.lower():
                return 'Y'

        else:
            return 'N'

    def convert_winding_rolwikkeling(rolwikkeling='outer_0'):
        # todo collect all rolwikkeling from printcom
        rolwikkel_dict = {
            "outer_180": 1,
            "outer_0": 2,
            "outer_270": 3,
            "outer_90": 4,

            "inner_180": 5,
            "inner_0": 6,
            "inner_270": 7,
            "inner_90": 8,

        }
        try:
            rolwikkeling_int = rolwikkel_dict[rolwikkeling]
            return rolwikkeling_int
        except KeyError:

            print(KeyError)
            return 2

    def convert_shape_into(shape='custom_shape'):
        if shape[0:8] == 'rectangle':
            return 'Rectangle'
        shape_dict = {
            'custom_shape': 'Irregular',
            'rectangle_sticker__2mm_rounded_corners': 'Rectangle',
            'rectangle_sticker_90_degree_angle': 'Rectangle',
            'circle_label': 'Circle'
        }
        try:
            shape = shape_dict[shape]
        except KeyError:
            shape = 'Irregular'

        return shape

    def radius(shape=None):
        # todo check if there isn't a radius in the json
        var = {
            'rectangle_sticker__2mm_rounded_corners': 2,
            'rectangle_sticker_90_degree_angle': 0
        }
        try:
            radi = var[shape]

        except KeyError:
            radi = 0

        return radi

    order_item_dict = asdict(order_item)
    designs = extract_design_info(order_item_dict)

    price = float(order_item.purchasePrice)
    copies_tot= int(options['copies'])

    pickup_date= str(order_item.pickupDate)[:10]

    price_per_1000_overall=price_per_1000(price, copies_tot)


    for design in designs:
        copies = design["copies"]

        price = order_item.purchasePrice

        width, height = calculate_dimensions_with_winding(options['width'], options['height'], convert_winding_rolwikkeling(options['output_direction']))
        print(options['output_direction'])
        print(convert_winding_rolwikkeling(str(options['output_direction'])))
        # Create an OrderInfo object for this design with the appropriate OrderQuantity
        order_info = OrderInfo(
            Description=verwijder_speciale_tekens(order_item.descriptions['full'][0:30]),
            ReferenceAtCustomer=order_item.orderItemNumber,
            LineComment1=str(order_item.orderItemNumber)[0:10],

            Delivery=pickup_date,  # due date
            Shipment_method=order_item.shipments[0]['method'],
            OrderQuantity=copies,  # Set the OrderQuantity based on the 'copies' value of the current design

            # Quantity_per_roll=verwijder_speciale_tekens(order_item.options['copies_per_roll']), # let op key niet aLTIJD AANWEXZIG
            Quantity_per_roll=order_item.options.get('copies_per_roll', ""),  # let op key niet aLTIJD AANWEXZIG
            Core=order_item.options.get('roll_diameter',''),

            # UnitPrice=price_per_1000(price, copies),  # Set the UnitPrice based on the 'price' value of the current design
            UnitPrice=price_per_1000_overall,  # Set the UnitPrice based on the 'price' value of the all design
            SupplierId='Print.com',
            Name=order_item.name,
            Street=verwijder_speciale_tekens(from_pdc_in_address.fullstreet),
            Country=verwijder_speciale_tekens(from_pdc_in_address.country),
            PostalCode=verwijder_speciale_tekens(from_pdc_in_address.postcode),
            City=verwijder_speciale_tekens(from_pdc_in_address.city),
            Contacts=[contact_from_first_shipment],
            Width=width,
            Height=height,
            Shape=convert_shape_into(options['shape']),
            Radius=radius(options['shape']),
            Winding=convert_winding_rolwikkeling(str(options['output_direction'])),
            Premium_White=check_for_white(order_item.pantoneColors),
            Substrate=order_item.options['material'],
            Adhesive=order_item.options['type_glue'],
        )
        all_order_info.append(order_info)

    return all_order_info


def process_order_item(sample_data: Dict[str, Any]) -> None:
    """
    Process an OrderItem object from a given dictionary.

    Args:
        sample_data (Dict[str, Any]): Dictionary containing the OrderItem data.

    Returns:
        None
    """
    try:
        order_item_object = OrderItem(**sample_data)
        contacts = order_item_object.shipments[0]['address']
        from_pdc_in_address = Address(**contacts)
        print(f'{order_item_object.name = }')

        order_info_for_cerm = convert_order_item_to_order_info(order_item_object)
        process_order_info_list(order_info_for_cerm)
        logging.info(f"OrderItem {order_item_object.orderItemNumber} processed successfully.")
        print('process_order_info_list: saved and processed')

    except Exception as e:
        logging.error(f"Error processing order item: {e}")
        print(f'process order item  Exception {str(e) = }')


def process_order_info_list(order_info_list: List[OrderInfo]):
    """Processes a list of OrderInfo objects.

    Args:
        order_info_list (List[OrderInfo]): The list of OrderInfo objects to process.

    Returns:
        None: The function performs its operations in-place or outputs to some external system.
    """
    for i, order_info in enumerate(order_info_list, 1):
        # Your processing logic here. For example:
        print(f"Processing order with ReferenceAtCustomer: {order_info.ReferenceAtCustomer}_{i}")
        print(f"  - OrderQuantity: {order_info.OrderQuantity}")
        logging.info(f"Processing order with ReferenceAtCustomer: {order_info.ReferenceAtCustomer}_{i}")
        logging.info(f"  - OrderQuantity: {order_info.OrderQuantity}")


        pad = Path(f'{DOWNLOAD_PAD}/{order_info.ReferenceAtCustomer}_{i}/{order_info.ReferenceAtCustomer}_{i}.json')
        print(pad)
        save_json(asdict(order_info), Path(pad))

        # zip time !
        uiteindelijkpad = Path(r'/Volumes/Esko/Vila-to-Esko/resellers') #macbook

        zip_folder(dest_zip=Path(f'{DOWNLOAD_PAD_VILA_TO_ESKO}/{order_info.ReferenceAtCustomer}_{i}'),
                   src_folder=Path(f'{DOWNLOAD_PAD}/{order_info.ReferenceAtCustomer}_{i}'))

        # zip_folder(dest_zip=Path(f'{testzip}/{order_info.ReferenceAtCustomer}_{i}'),
        #            src_folder=Path(f'{DOWNLOAD_PAD}/{order_info.ReferenceAtCustomer}_{i}'))

        #
