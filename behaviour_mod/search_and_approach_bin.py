from behaviour_mod.behaviour import Behaviour
from robobopy.utils.IR import IR
from robobopy.utils.Sounds import Sounds
from robobopy.utils.Emotions import Emotions

class SearchAndApproachBin(Behaviour):
    def __init__(self, robot, supress_list, params):
        super().__init__(robot, supress_list, params)
        self.completed = False

    def take_control(self):
        # Take control if an object has been approached and bin not yet found, and not suppressed
        return self.params.get('approached_obj') is not None and not self.completed and not self.supress

    def classify_object(self, obj):
        if obj.label.lower() in ["bottle", "container"]:
            return "plastic"
        elif obj.label.lower() in ["apple", "banana", "orange"]:
            return "organic"
        elif obj.label.lower() in ["paper", "cup", "newspaper", "flyer"]:
            return "paper"

    def action(self):
        print("----> control: SearchAndApproachBin")
        self.supress = False
        for bh in self.supress_list:
            bh.supress = True

        obj = self.params.get('approached_obj')
        if obj is None:
            print("No object to classify.")
            return
        category = self.classify_object(obj)
        print(f"Object classified as: {category}")
        self.params['object_category'] = category

        self.robot.moveTiltTo(90, 5, True)
        mission = False
        for i in range(95):  # Rotate to left and look for QR
            if mission:
                break
            ir_value = self.robot.readIRSensor(IR.FrontC)

            if i<15 or 50<i<70:
                self.robot.moveWheelsByTime(2, -2, 0.5)
                if i%2==0:#Move forward to not lose the object, every 2loops
                    self.robot.moveWheelsByTime(5, 5, 0.2)
            elif 15<i<50 or 65<i<110:
                self.robot.moveWheelsByTime(-2, 2, 0.6)
                if i%2==0:#Move forward to not lose the object, every 2loops
                    self.robot.moveWheelsByTime(5, 5, 0.2) 
            elif i==50:
                self.robot.moveWheelsByTime(5, 5, 2)
                print("move forward")
            qr = self.robot.readQR()
            print("loop", i + 1)
            if qr is not None and category.lower() == qr.id.lower():
                print("Found bin for:", category)
                while True:
                    if self.supress:
                        break
                    qr = self.robot.readQR()
                    print("We are", qr.distance, "% close")
                    if qr.distance > 90:
                        self.robot.stopMotors()
                        print("Reached the bin. Stopping.")
                        self.robot.playSound(Sounds.LIKES)
                        self.robot.setEmotionTo(Emotions.HAPPY)      # Show happy face
                        self.robot.sayText("mission completed!")          # Say something happy
                        mission = True
                        self.completed = True
                        self.params['stop'] = True  # Signal mission complete
                        break
                    if qr.x < 180:
                        self.robot.moveWheelsByTime(-2, 2, 0.1)
                    elif qr.x > 220:
                        self.robot.moveWheelsByTime(2, -2, 0.1)
                    else:
                        self.robot.moveWheelsByTime(6, 6, 0.6)
        self.robot.stopMotors() 