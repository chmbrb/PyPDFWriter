from typing import Any
from dataclasses import dataclass


@dataclass
class Entity:
    '''Generic entity object used to represent employers and agents'''

    entity_id: int
    fname: str
    lname: str
    job: str
    payrate: float
    ssn: str
    dob: str
    phone: str
    email: str
    address: str
    city: str
    state: str
    zipcode: str

    @staticmethod
    def from_dict(obj: Any) -> 'Entity':
        _entity_id = int(obj.get("id"))
        _fname = str(obj.get("fname"))
        _lname = str(obj.get("lname"))
        _job = str(obj.get("job"))
        _payrate = float(obj.get("payrate"))
        _ssn = str(obj.get("ssn"))
        _dob = str(obj.get("dob"))
        _phone = str(obj.get("phone"))
        _email = str(obj.get("email"))
        _address = str(obj.get("address"))
        _city = str(obj.get("city"))
        _state = str(obj.get("state"))
        _zipcode = str(obj.get("zipcode"))
        return Entity(_entity_id, _fname, _lname, _job, _payrate, _ssn, _dob, _phone, _email, _address, _city, _state, _zipcode)