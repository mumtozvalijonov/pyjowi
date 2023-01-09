from datetime import date
from enum import Enum
from typing import List, Optional

from ._base import JowiRequestModel, JowiResponseModel


class OrderType(int, Enum):
    DELIVERY = 0
    TAKEAWAY = 1


class PaymentMethod(int, Enum):
    ON_DELIVERY = 0
    ONLINE = 1


class PaymentType(int, Enum):
    CASH = 0
    CARD = 1


class CancellationType(int, Enum):
    RESTAURANT = 0
    CLIENT = 1


class OrderStatus(int, Enum):
    NEW = 0
    ACCEPTED = 1
    CANCELLED = 2
    SENT = 3
    DELIVERED = 4


class CreateOrderCourse(JowiRequestModel):
    course_id: str
    count: int
    description: Optional[str]

    def to_jowi_request(self) -> dict:
        return {
            'course_id': self.course_id,
            'count': self.count,
            'description': self.description
        }


class CreateOrderDTO(JowiRequestModel):
    api_key: Optional[str]
    signature: Optional[str]
    restaurant_id: str
    address: Optional[str]
    total_price: float
    description: Optional[str]
    order_type: OrderType = OrderType.DELIVERY
    payment_method: PaymentMethod = PaymentMethod.ON_DELIVERY
    payment_type: PaymentType = PaymentType.CASH
    people_count: int
    contact_name: str
    contact_phone: str
    courses: List[CreateOrderCourse]

    def to_jowi_request(self) -> dict:
        return {
            'api_key': self.api_key,
            'sig': self.signature,
            'restaurant_id': self.restaurant_id,
            'order': {
                'address': self.address,
                'amount_order': self.total_price,
                'description': self.description,
                'order_type': self.order_type.value,
                'payment_method': self.payment_method.value,
                'payment_type': self.payment_type.value,
                'people_count': self.people_count,
                'contact': self.contact_name,
                'phone': self.contact_phone,
                'courses': [course.to_jowi_request() for course in self.courses]
            }
        }


class OrderCourse(JowiResponseModel):
    id: str
    count: float
    price: float
    course_id: str
    course_price: float
    description: Optional[str]
    is_exception: bool = False


class Order(JowiResponseModel):
    id: str
    address: Optional[str]
    total_price: float
    cancellation_reason: Optional[str]
    cancellation_type: CancellationType = CancellationType.RESTAURANT
    contact_name: str
    contact_phone: str
    courier_name: Optional[str]
    courier_phone: Optional[str]
    created_at: str
    delivery_price: float
    description: Optional[str]
    discount: float = 0
    is_cancellation_confirmed: bool = False
    is_delivery_in_cash: bool = False
    is_paid: bool = False
    number: Optional[int]
    order_type: OrderType = OrderType.DELIVERY
    payment_method: PaymentMethod = PaymentMethod.ON_DELIVERY
    payment_type: PaymentType = PaymentType.CASH
    people_count: int
    restaurant_id: str
    status: OrderStatus
    work_date: date
    courses: List[OrderCourse]


class CancelOrderDTO(JowiRequestModel):
    api_key: Optional[str]
    signature: Optional[str]
    order_id: str
    cancellation_reason: str

    def to_jowi_request(self) -> dict:
        return {
            'api_key': self.api_key,
            'sig': self.signature,
            'cancellation_reason': self.cancellation_reason,
        }
