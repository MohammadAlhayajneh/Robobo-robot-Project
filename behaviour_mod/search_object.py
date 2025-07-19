from behaviour_mod.behaviour import Behaviour
from robobopy.utils.Sounds import Sounds
from robobopy.utils.Emotions import Emotions


class SearchObject(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.found_obj = None

    def take_control(self):
        # Run if we haven't found an object yet and not suppressed
        return self.found_obj is None and not self.supress

    def action(self):
        print("----> control: SearchObject")
        self.robot.playSound(Sounds.THINKING)
        self.supress = False
        for bh in self.supress_list:
            bh.supress = True

        self.robot.moveTiltTo(100, 5, True)  # Tilt camera down

        # First search rotating left
        for _ in range(5):
            if self.supress:
                break
            self.robot.moveWheelsByTime(2, -2, .2)
            self.robot.startObjectRecognition()
            obj = self.robot.readDetectedObject()
            self.robot.stopObjectRecognition()
            if obj.label != "":
                print("Found on left:", obj.label)
                if obj.x < 180:
                    self.robot.moveWheelsByTime(2, -2, 0.2)
                elif obj.x > 220:
                    self.robot.moveWheelsByTime(-2, 2, 0.2)
                self.found_obj = obj
                self.params['detected_obj'] = obj  # Share with other behaviors
                self.robot.playSound(Sounds.OUCH)
                self.robot.setEmotionTo(Emotions.HAPPY) 
                self.robot.sayText("We found something")
                break

        # Then search rotating right
        if not self.found_obj:
            for _ in range(2):
                if self.supress:
                    break
                self.robot.moveWheelsByTime(-2, 2, .2)
                self.robot.startObjectRecognition()
                obj = self.robot.readDetectedObject()
                self.robot.stopObjectRecognition()
                if obj.label != "":
                    print("Found on right:", obj.label)
                    if obj.x < 180:
                        self.robot.moveWheelsByTime(2, -2, 0.2)
                    elif obj.x > 220:
                        self.robot.moveWheelsByTime(-2, 2, 0.2)
                    self.found_obj = obj
                    self.params['detected_obj'] = obj
                    self.robot.playSound(Sounds.OUCH)
                    self.robot.setEmotionTo(Emotions.HAPPY)
                    self.robot.sayText("We found something") 
                    break

        if not self.found_obj:
            print("No object found")
        self.robot.stopMotors() 