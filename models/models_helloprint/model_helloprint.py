from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Address:
    addressType: Optional[str] = field(default=None)
    lastname: Optional[str] = field(default=None)
    company: Optional[str] = field(default=None)
    firstname: Optional[str] = field(default=None)
    address1: Optional[str] = field(default=None)
    address2: Optional[str] = field(default=None)
    postcode: Optional[str] = field(default=None)
    city: Optional[str] = field(default=None)
    country: Optional[str] = field(default=None)
    phone: Optional[str] = field(default=None)
    mobilePhone: Optional[str] = field(default=None)
    email: Optional[str] = field(default=None)





@dataclass
class Product:
    quantity: Optional[int] = field(default=None)
    productName: Optional[int] = field(default=None)
    attributes: Optional[int] = field(default=None)


@dataclass
class FilesToDownload:
    packingSlipUrl: Optional[str] = field(default=None)
    shippingLabelUrl: Optional[str] = field(default=None)
    filename: Optional[str] = field(default=None)


@dataclass
class OrderLine:
    orderId: Optional[int] = field(default=None)
    orderDetailId: Optional[int] = field(default=None)
    customerId: Optional[int] = field(default=None)
    md5Value: Optional[str] = field(default=None)
    sku: Optional[str] = field(default=None)
    weight: Optional[float] = field(default=None)
    pageCount: Optional[int] = field(default=None)
    supplierSku: Optional[str] = field(default=None)
    carrierName: Optional[str] = field(default=None)
    targetDispatchDate: Optional[str] = field(default=None)
    purchasePrice: Optional[float] = field(default=None)
    productName: Optional[str] = field(default=None)
    slaDays: Optional[int] = field(default=None)
    dateDeadline: Optional[str] = field(default=None)
    skipQueue: Optional[int] = field(default=None)
    productionDays: Optional[int] = field(default=None)
    files_to_download: Optional[FilesToDownload] = field(default=None)
    address: Optional[Address] = field(default=None)
    product: Optional[Product] = field(default=None)
    idCustomer: Optional[Product] = field(default=None)

    product_type: Optional[str] = field(default=None),
    materiaal: Optional[str] = field(default=None),
    materiaal_description: Optional[str] = field(default=None),
    dimensions: Optional[str] = field(default=None),
    quantity: Optional[str] = field(default=None),
    kern: Optional[str] = field(default=None),
    shape: Optional[str] = field(default=None),
    width: Optional[str] = field(default=None),
    height: Optional[str] = field(default=None),
    other_info: Optional[str] = field(default=None),





@dataclass
class Order:
    orderId: Optional[int] = field(default=None)
    orderLines: List[Optional[OrderLine]] = field(default_factory=list)


@dataclass
class Root:
    orders: List[Optional[Order]] = field(default_factory=list)


class FromSku:
    ...
