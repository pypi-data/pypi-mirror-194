""" Base class that instantiate robot control """
from abc import ABC
from covmatic_stations.station import Station, instrument_loader, labware_loader
from .robot import Robot


class RobotStationABC(Station, ABC):
    def __init__(self,
                 ot_name: str,
                 robot_manager_host: str = None,
                 robot_manager_port: int = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ot_name = ot_name
        self._robot_manager_host = robot_manager_host
        self._robot_manager_port = robot_manager_port

    @instrument_loader(0, "_robot")
    def load_robot(self):
        self._robot = Robot(robot_name=self._ot_name,
                            robot_manager_host=self._robot_manager_host,
                            robot_manager_port=self._robot_manager_port,
                            simulate=self._ctx.is_simulating())

    def robot_pick_plate(self, slot, plate_name):
        if self._run_stage:
            self.home()
            try:
                self._robot.pick_plate(slot, plate_name)
            except Exception as e:
                self.logger.error("Error requesting pick plate {} from slot {}: {}".format(plate_name, slot, e))
                self.pause("Error in plate transfer. Please transfer manually plate {} from slot {}".format(plate_name, slot),
                           home=False)
        else:
            self.logger.info("Skipping pick plate {} from slot {} because previous stage not run.")

    def robot_drop_plate(self, slot, plate_name):
        if self._run_stage:
            self.home()
            try:
                self._robot.drop_plate(slot, plate_name)
            except Exception as e:
                self.logger.error("Error requesting drop plate {} to slot {}: {}".format(plate_name, slot, e))
                self.pause("Error in plate transfer. Please transfer manually plate {} to slot {}".format(plate_name, slot),
                           home=False)
        else:
            self.logger.info("Skipping pick plate {} from slot {} because previous stage not run.")
