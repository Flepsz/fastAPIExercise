from pydantic import BaseModel

class Item(BaseModel):
    company: str


fakeDatabase = {
    1: {'company': '45.990.181/0001-89'},
    2: {'company': '00.776.574/0001-56'},
    3: {'company': '15.436.940/0001-03'},
    4: {'company': '39.672.219/0001-72'},
    5: {'company': '06.947.283/0001-60'},
    6: {'company': '05.720.854/0001-66'},
    7: {'company': '59.275.792/0001-50'},
    8: {'company': '92.754.738/0001-62'},
    9: {'company': '00.280.273/0002-18'},
    10: {'company': '60.500.139/0001-26'},
}