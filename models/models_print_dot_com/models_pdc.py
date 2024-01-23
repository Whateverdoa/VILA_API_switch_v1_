from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional


@dataclass
class Address:
    """Dataclass for Address."""

    id: Optional[int] = field(default=None)
    city: Optional[str] = field(default=None)
    email: Optional[str] = field(default=None)
    street: Optional[str] = field(default=None)
    country: Optional[str] = field(default=None)
    lastName: Optional[str] = field(default=None)
    postcode: Optional[str] = field(default=None)
    firstName: Optional[str] = field(default=None)
    telephone: Optional[str] = field(default=None)
    fullstreet: Optional[str] = field(default=None)
    companyName: Optional[str] = field(default=None)
    houseNumber: Optional[str] = field(default=None)
    extraAddressLine: Optional[str] = field(default=None)


@dataclass
class Shipment:
    """Dataclass for Shipment."""

    address: Address

    tax: Optional[float] = field(default=1.5)
    copies: Optional[int] = field(default=None)
    method: Optional[str] = field(default=None)

    addressId: Optional[int] = field(default=None)
    pickedUpBy: Any = field(default=None)
    shipmentId: Optional[str] = field(default=None)
    normalPrice: Optional[int] = field(default=None)
    deliveryDate: Optional[str] = field(default=None)
    productDiscount: Optional[int] = field(default=None)
    storageLocation: Any = field(default=None)
    printCustomLabel: bool = field(default=False)
    shippingDiscount: Optional[int] = field(default=None)
    shippingLabelUrl: Optional[str] = field(default=None)
    combinedShipmentId: Optional[Any] = field(default=None)
    latestDeliveryDate: Optional[str] = field(default=None)
    combinedShipmentDiscount: Optional[int] = field(default=None)
    orderItemsWithSameShippingAddress: List[Any] = field(default_factory=list)
    designs: Optional[List[Dict[str, Any]]] = field(default_factory=list)


@dataclass
class Design:
    """Dataclass for Design."""

    id: Optional[int] = field(default=None)
    href: Optional[str] = field(default=None)
    copies: Optional[int] = field(default=1)
    shipments: List[Shipment] = field(default_factory=list)


@dataclass
class Options:
    """Dataclass for Options."""

    size: Optional[str] = field(default=None)
    shape: Optional[str] = field(default=None)
    width: Optional[str] = field(default=None)
    copies: Optional[str] = field(default=None)
    copies_per_roll: Optional[str] = field(default=None)
    finish: Optional[str] = field(default=None)
    height: Optional[str] = field(default=None)
    urgency: Optional[str] = field(default=None)
    material: Optional[str] = field(default=None)
    squareMM: Optional[str] = field(default=None)
    printtype: Optional[str] = field(default=None)
    type_glue: Optional[str] = field(default=None)
    planoWidth: Optional[str] = field(default=None)
    planoHeight: Optional[str] = field(default=None)
    roll_diameter: Optional[str] = field(default=None)
    printingmethod: Optional[str] = field(default=None)
    numberOfDesigns: Optional[str] = field(default=None)
    output_direction: Optional[str] = field(default=None)
    number_of_stickers: Optional[str] = field(default=None)


@dataclass
class Descriptions:
    """Dataclass for Descriptions."""

    full: Optional[str] = field(default=None)
    size: Optional[str] = field(default=None)
    designs: Optional[int] = field(default=1)
    material: Optional[str] = field(default=None)
    printing: Optional[str] = field(default=None)
    shipping: Optional[str] = field(default=None)
    finishing: Optional[str] = field(default=None)


@dataclass
class OrderItem:
    """Dataclass for OrderItem."""

    sku: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    _links: Dict[str, Dict[str, str]] = field(default_factory=dict)
    status: Optional[str] = field(default=None)
    created: Optional[str] = field(default=None)
    designs: List[Any] = field(default_factory=list)
    layouts: List[Any] = field(default_factory=list)
    options: Any = field(default=None)
    orderId: Optional[int] = field(default=None)
    variants: List[Any] = field(default_factory=list)
    shipments: List[Any] = field(default_factory=list)
    childItems: List[Any] = field(default_factory=list)
    pickupDate: Optional[str] = field(default=None)
    printjobId: Optional[str] = field(default=None)
    orderItemId: Optional[int] = field(default=None)
    orderNumber: Optional[int] = field(default=None)
    urgencyCost: Optional[int] = field(default=None)
    descriptions: Any = field(default=None)
    supplierCode: Optional[str] = field(default="VE")
    pantoneColors: List[Any] = field(default_factory=list)
    # purchasePrice: Optional[str] = field(default='0.0')
    purchasePrice: float = field(default=0.0)
    quantity: int = field(default=0)
    submissionDate: Optional[str] = field(default=None)
    deliveryPromise: Optional[int] = field(default=None)
    orderItemNumber: Optional[str] = field(default=None)
    supplierChecklist: List[Any] = field(default_factory=list)
    deliveryPromiseCost: Optional[int] = field(default=None)
    designsHasSameAmount: bool = field(default=False)
    reprintCreditUrgency: Optional[int] = field(default=None)
    reprintCreditDeliveryPromise: Optional[int] = field(default=None)
    note: Optional[str] = field(default=None)
    reprintOrderItemNumber: Optional[str] = field(default=None)
    preferredLanguage: Optional[str] = field(default=None)