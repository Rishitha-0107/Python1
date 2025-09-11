from abc import ABC,abstractmethod
import time
class Vehicle:
    def __init__(self, license_plate, owner_name):
        self.__license_plate = license_plate   
        self.__owner_name = owner_name         
    def get_license_plate(self):
        return self.__license_plate
    def set_license_plate(self, plate):
        self.__license_plate = plate
    def get_owner_name(self):
        return self.__owner_name
    def set_owner_name(self, name):
        self.__owner_name = name
    def display(self):
        print("Generic Vehicle")
    def calculate_parking_fee(self, hours):
        return 0
class Bike(Vehicle):
    def __init__(self, license_plate, owner_name, helmet_required=True):
        super().__init__(license_plate, owner_name)
        self.helmet_required = helmet_required
    def display(self):
        print(f"Bike | Plate: {self.get_license_plate()} | Owner: {self.get_owner_name()} | Helmet Required: {self.helmet_required}")
    def calculate_parking_fee(self, hours):
        return 20 * hours
class Car(Vehicle):
    def __init__(self, license_plate, owner_name, seats=4):
        super().__init__(license_plate, owner_name)
        self.seats = seats
    def display(self):
        print(f"Car | Plate: {self.get_license_plate()} | Owner: {self.get_owner_name()} | Seats: {self.seats}")
    def calculate_parking_fee(self, hours):
        return 50 * hours
class SUV(Vehicle):
    def __init__(self, license_plate, owner_name, four_wheel_drive=True):
        super().__init__(license_plate, owner_name)
        self.four_wheel_drive = four_wheel_drive
    def display(self):
        print(f"SUV | Plate: {self.get_license_plate()} | Owner: {self.get_owner_name()} | 4WD: {self.four_wheel_drive}")
    def calculate_parking_fee(self, hours):
        return 70 * hours
class Truck(Vehicle):
    def __init__(self, license_plate, owner_name, max_load_capacity=10000):
        super().__init__(license_plate, owner_name)
        self.max_load_capacity = max_load_capacity
    def display(self):
        print(f"Truck | Plate: {self.get_license_plate()} | Owner: {self.get_owner_name()} | Max Load: {self.max_load_capacity}kg")
    def calculate_parking_fee(self, hours):
        return 100 * hours
class ParkingSpot:
    def __init__(self, spot_id, size):
        self.__spot_id = spot_id   # private
        self.__size = size         # S, M, L, XL
        self.__is_free = True
        self.__vehicle = None
        self.__entry_time = None
    def get_size(self):
        return self.__size
    def is_available(self):
        return self.__is_free
    def assign_vehicle(self, vehicle):
        if not self.__is_free:
            print(f"Spot {self.__spot_id} already occupied!")
            return False
        self.__vehicle = vehicle
        self.__is_free = False
        self.__entry_time = time.time()
        print(f"Vehicle {vehicle.get_license_plate()} parked in Spot {self.__spot_id}")
        return True
    def remove_vehicle(self):
        if self.__is_free:
            print(f"Spot {self.__spot_id} is already empty.")
            return None, 0
        exit_time = time.time()
        hours = max(1, int((exit_time - self.__entry_time) // 3600 + 1))  # at least 1 hour
        fee = self.__vehicle.calculate_parking_fee(hours)
        print(f"Vehicle {self.__vehicle.get_license_plate()} un-parked from Spot {self.__spot_id}")
        vehicle = self.__vehicle
        self.__vehicle = None
        self.__is_free = True
        self.__entry_time = None
        return vehicle, fee
    def show_status(self):
        status = "Free" if self.__is_free else f"Occupied by {self.__vehicle.get_license_plate()}"
        print(f"Spot {self.__spot_id} ({self.__size}) → {status}")
class ParkingLot:
    def __init__(self):
        self.spots = []
    def add_spot(self, spot):
        self.spots.append(spot)
    def show_spots(self):
        for spot in self.spots:
            spot.show_status()
    def park_vehicle(self, vehicle):
        size_requirement = {
            Bike: ["S", "M", "L", "XL"],
            Car: ["M", "L", "XL"],
            SUV: ["L", "XL"],
            Truck: ["XL"]
        }

        for spot in self.spots:
            if spot.is_available() and spot.get_size() in size_requirement[type(vehicle)]:
                return spot.assign_vehicle(vehicle)

        print(f"No suitable spot available for {vehicle.get_license_plate()}")
        return False

    def unpark_vehicle(self, vehicle):
        for spot in self.spots:
            if not spot.is_available() and spot._ParkingSpot__vehicle == vehicle:  # Access private via name-mangling
                vehicle, fee = spot.remove_vehicle()
                return fee
        print(f"Vehicle {vehicle.get_license_plate()} not found in parking lot.")
        return 0
class Payment(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass
class CashPayment(Payment):
    def process_payment(self, amount):
        print(f"Paid ₹{amount} in cash")
class CardPayment(Payment):
    def process_payment(self, amount):
        print(f"Paid ₹{amount} using Credit/Debit Card")
class UPIPayment(Payment):
    def process_payment(self, amount):
        print(f"Paid ₹{amount} via UPI")
if __name__ == "__main__":
    # Create parking lot
    lot = ParkingLot()
    lot.add_spot(ParkingSpot(1, "S"))
    lot.add_spot(ParkingSpot(2, "M"))
    lot.add_spot(ParkingSpot(3, "L"))
    lot.add_spot(ParkingSpot(4, "XL"))
    # Create vehicles
    v1 = Bike("TS09AB1234", "Ravi")
    v2 = Car("TS09XY5678", "Anjali", 5)
    v3 = SUV("TS10PQ1111", "Krishna")
    v4 = Truck("TS11LM2222", "Mahesh", 20000)
    lot.park_vehicle(v1)
    lot.park_vehicle(v2)
    lot.park_vehicle(v3)
    lot.park_vehicle(v4)
    print("\n--- Parking Lot Status ---")
    lot.show_spots()
    print("\n--- Unparking Vehicle ---")
    fee = lot.unpark_vehicle(v2)
    if fee > 0:
        payment_method = UPIPayment()  
        payment_method.process_payment(fee)
    print("\n--- Final Parking Lot Status ---")
    lot.show_spots()
