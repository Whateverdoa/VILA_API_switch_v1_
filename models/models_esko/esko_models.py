from dataclasses import dataclass, field
from typing import List, Union, Optional


# Define helloprint_converted_dataclass Contact dataclass
@dataclass
class Contact:
    LastName: str
    FirstName: str
    Initials: str
    Title: str
    PhoneNumber: str
    FaxNumber: str
    GSMNumber: str
    Email: str
    Function: str


# Define helloprint_converted_dataclass Delivery dataclass
@dataclass
class Delivery:
    Type: str
    Comment: str
    AddressId: str
    ExpectedDate: str


# Define the main OrderInfo dataclass
@dataclass
class OrderInfo:

    Description: str
    ReferenceAtCustomer: str
    Delivery: str  # due date
    Shipment_method: str
    OrderQuantity: Union[int, str]
    Quantity_per_roll: str
    Core: str
    UnitPrice: float
    SupplierId: str
    Name: str
    Street: str
    Country: str
    PostalCode: str
    City: str
    Contacts: List[Contact]

    Width: str
    Height: str

    Shape: str  # def for conversion
    Winding: int  # def for conversion
    Radius: float  # def for conversion
    Premium_White: str  # def for conversion if pantone contains white
    Substrate: str
    Adhesive: str


    LineComment1: Optional[str] = field(default=None)


# Sample usage
# Assuming `json_data` is helloprint_converted_dataclass dictionary containing your JSON data
# order_info_instance = OrderInfo(**json_data)

# To convert the dataclass instance to helloprint_converted_dataclass dictionary
# order_info_dict = asdict(order_info_instance)

# To export the dataclass instance as helloprint_converted_dataclass JSON file
# with open('order_info.json', 'w') as f:
#     json.dump(order_info_dict, f, indent=4)

# The dataclass can now be used to instantiate objects that represent the given JSON structure.
