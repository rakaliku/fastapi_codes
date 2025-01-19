from datetime import datetime
from pydantic import BaseModel, PositiveInt, ValidationError


class User(BaseModel):
    id: int
    name: str = 'Rk'
    signup_ts:datetime | None
    tastes: dict[str, PositiveInt]


external_data = {
    'id': 'not an int',
    'signup_ts': '2019-06-01 12:22',  
    'tastes': {
        'wine': 9,
        b'cheese': 7,  
        'cabbage': '1',  
    },
}

try:
    user = User(**external_data)
except ValidationError as e:
    # print(e.errors)
    print(e)

# print(user.model_dump())
# print(type(user.model_dump()))
# print(user.id)
# print(type(user.id))