from typing import Optional, List

from ._base import JowiBaseModel


class Table(JowiBaseModel):
    id: str
    hall_id: str
    is_time_discount: bool
    is_time_service: bool
    deposit: float
    number: int
    type: str
    num_seats: int

    @classmethod
    def from_jowi_response(cls, response: dict) -> List['Table']:
        tables: List[Table] = []
        hall_id = response['hall_id']
        for plain_meta in response['plain'].values():
            table: 'Table' = None
            num_seats = 0
            for item in plain_meta['item']:
                if item.get('id'):
                    if table:
                        table.num_seats = num_seats
                        tables.append(table)
                        num_seats = 0
                    table = cls(
                        id=item['id'],
                        hall_id=hall_id,
                        number=item['number'],
                        type=item['type'],
                        is_time_discount=item['is_time_discount'],
                        is_time_service=item['is_time_service'],
                        deposit=item['deposit'],
                        num_seats=0,
                    )
                else:
                    num_seats += 1
        return tables


class Hall(JowiBaseModel):
    id: str
    title: str
    restaurant_id: Optional[str]
    tables: Optional[List[Table]]

    @classmethod
    def from_jowi_response(cls, response: dict) -> List['Hall']:
        data = response.get('halls')
        return [cls(**hall) for hall in data]
