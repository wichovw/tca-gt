import tca_ng.cells


class ProvisionalCar:
    speed = 0
    cell = None
    
    def __init__(self, car):
        self.speed = car.speed
        self.cell = car.cell


class Car:
    id = 0
    cell = None
    speed = 0
    route = None
    v_max = 3
    p = None
    
    decelerate_rate = 0.3
    # Que tan agresivo es el carro para cambiar de carriles
    base_lane_changing_rate = 0.2
    # Que tan agresivo es en este momento el carro para cambiar de carril
    lane_changing_rate = 0.2
    # Que tan probable es que cambie a la derecha. Complemento a la izquierda
    right_change_rate = 0.5
    # Cuantas iteraciones esperaría al final de una calle para cambiar de carril
    # antes de cambiar de ruta
    changing_route_max_wait = 10
    # Cuantas iteraciones lleva esperando al final de una calle tratando de cambiar de carril
    waits_for_lane_change = 0
    
    def __init__(self):
        self.id = Car.id
        Car.id += 1
    
    def __repr__(self):
        return "<Car: %s (%s)>" % (self.id, self.speed)
    
    def apply_rules(self):
        if isinstance(self.p.cell, tca_ng.cells.StreetCell):
            if not isinstance(self.cell, tca_ng.cells.StreetCell) or (
                self.cell.street != self.p.cell.street
            ):
                    self.p.cell.street.car_entry(self)
        self.speed = self.p.speed
        self.cell = self.p.cell