import datetime
import uuid


class Request:

    def __init__(self):
        self.function = None
        self.equipments = []
        self.start = None
        self.end = None
        self.aggregation = None
        self.interval = None
        self.filters = None
        self.on_off_sensor = None
        self.restart_time = None
        self.sensitivity = None
        self.dataframe = None
        self.extra_data = None
        self.target_feat = None
        self.connections = None
        self.name = None

    def prepare(self):
        query = {}
        if self.equipments is not None:
            query["equipments_list"] = self.equipments
        if self.start is not None and self.end is not None:
            query["timeframe"] = {
                "start": self.__format_date(self.start),
                "end": self.__format_date(self.end)
            }
        return query

    def __format_date(self, dt_to_format):
        if isinstance(dt_to_format, datetime.datetime):
            millisec = dt_to_format.timestamp() * 1000
            return int(millisec)
        else:
            raise TypeError("date is not a valid datetime")

    def add_datapoints(self, equipment_id: uuid.UUID, datapoints, shift=0):
        if equipment_id is not None and not isinstance(equipment_id, uuid.UUID):
            raise TypeError("equipment_id must be None or of type uuid.UUID")
        for equipment in self.equipments:
            if "id" in equipment.keys() and equipment["id"] == str(equipment_id):
                raise ValueError("equipment_id is already in the request please remove it before adding datapoints.")
        self.equipments.append({
            "id": str(equipment_id),
            "datapoints": datapoints,
            "shift": str(shift) + "s"
        })

    # attempt to remove equipment from the query if exists
    def remove_equipment(self, equipment_id: uuid.UUID):
        if equipment_id is not None and not isinstance(equipment_id, uuid.UUID):
            raise TypeError("equipment_id must be None or of type uuid.UUID")
        found = None
        for equipment in self.equipments:
            if "id" in equipment.keys() and equipment["id"] == str(equipment_id):
                found = equipment
        if found is not None:
            self.equipments.remove(equipment)

