class Units:
    def __init__(self, UnitId, location, size, status, rent, sellingprice):
        self.UnitId = UnitId
        self.location = location
        self.size = size
        self.status = status 
        self.rent = rent
        self.sellingprice = sellingprice

    def markedasRented(self):
        self.status = "Rented"

    def markedasSold(self):
        self.status = "Sold"
    
    def __str__(self):
        return f"{self.UnitId.title()} | {self.location} | ${self.size} | {self.status} | ${self.rent} | ${self.sellingprice}"

# to check if it works
if __name__ == "__main__":
    unit = Units("unit101", "Downtown", 1200, "Rented", None, 300000)
    if unit.status == "Rented":
        unit.markedasRented()
    print(unit)

    # unit.markedasRented()
    # print(unit)