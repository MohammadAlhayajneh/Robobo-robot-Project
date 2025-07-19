from behaviour_mod.behaviour import Behaviour
from robobopy.utils.IR import IR

class ApproachObject(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.approached = False

    def take_control(self):
        # Take control if an object has been detected and not yet approached, and not suppressed
        return self.params.get('detected_obj') is not None and not self.approached and not self.supress

    def action(self):
        print("----> control: ApproachObject")
        self.supress = False
        for bh in self.supress_list:
            bh.supress = True

        while True:
            if self.supress:
                break
            self.robot.startObjectRecognition()
            obj = self.robot.readDetectedObject()
            self.robot.stopObjectRecognition()

            if obj.label != "":
                self.dobj=obj
                print("Approaching:", obj.label, "x =", obj.x, "y =", obj.y)
                # Use x-coordinate to adjust direction
                if obj.x > 220:
                    self.robot.moveWheelsByTime(2, -2, 0.2)  # Turn left slightly
                elif obj.x < 180:
                    self.robot.moveWheelsByTime(-2, 2, 0.2)  # Turn right slightly
                else:
                    ir_value = self.robot.readIRSensor(IR.FrontC)
                    print("ir = ", ir_value)
                    self.robot.moveWheelsByTime(15, 15, 0.4)  # Move forward
                # Stop if object is close (based on IR)
                ir_value = self.robot.readIRSensor(IR.FrontC)
                ir_value2 = self.robot.readIRSensor(IR.FrontL)
                ir_value3 = self.robot.readIRSensor(IR.FrontR)
                if ir_value >250 and ir_value2 >100 and ir_value3 >100 :
                    self.robot.stopMotors()
                    print("Close enough. Stopping.")
                    self.approached = True
                    self.params['approached_obj'] = obj
                    break
            else:
                ir_value = self.robot.readIRSensor(IR.FrontC)
                ir_value2 = self.robot.readIRSensor(IR.FrontL)
                ir_value3 = self.robot.readIRSensor(IR.FrontR)
                if ir_value >250 and ir_value2 >150 and ir_value3 >150 :
                    self.robot.stopMotors()
                    print("Close enough. Stopping.")
                    print("the returned object is ",self.dobj.label)
                    self.approached = True
                    self.params['approached_obj'] = self.dobj
                    break
                self.robot.moveWheelsByTime(4, 4, 0.2)  # Move forward
        self.robot.stopMotors() 