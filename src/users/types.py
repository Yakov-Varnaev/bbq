from datetime import datetime
from typing import TypedDict


class UserData(TypedDict, total=False):
    username: str
    first_name: str
    last_name: str
    email: str
    is_superuser: bool
    is_staff: bool
    is_active: bool
    date_joined: datetime
    bio: str
