import wpilib
import ctre
from wpilib.drive import DifferentialDrive
from wpilib.interfaces import GenericHID

#MOTOR PARTS
LEFT = 1
RIGHT = 3
CENTER1 = 2
CENTER2 = 4

#BALL MANIPULATOR
BALL_MANIP_ID = 5
GATHER_SPEED = 1.0
SPIT_SPEED = -1.0
STOP_SPEED = 0.0

LEFT_HAND = GenericHID.Hand.kLeft
RIGHT_HAND = GenericHID.Hand.kRight

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        """
        Initializes all motors in the robot.
        """
        
        self.leftVictor = ctre.WPI_VictorSPX(LEFT)
        self.rightVictor = ctre.WPI_VictorSPX(RIGHT)
        self.centerVictor1 = ctre.WPI_VictorSPX(CENTER1)
        self.centerVictor2 = ctre.WPI_VictorSPX(CENTER2)

        self.left = wpilib.SpeedControllerGroup(self.leftVictor)
        self.right = wpilib.SpeedControllerGroup(self.rightVictor)

        self.center1 = wpilib.SpeedControllerGroup(self.centerVictor1)
        self.center2 = wpilib.SpeedControllerGroup(self.centerVictor2)

        self.myRobot = DifferentialDrive(self.right, self.left)
        self.myRobot.setExpiration(0.1)

        #  reasonable deadzone size
        self.DEADZONE = 0.1

        self.driver = wpilib.XboxController(0)
        
    def autonomousInit(self):
        pass #Do nothing for now in auton

    def autonomousPeriodic(self):
        pass #Do nothing for now in auton

    def teleopInit(self):
        """
        Huh?
        """
        self.myRobot.setSafetyEnabled(True)

    def deadzone(self, val, deadzone):
        if abs(val) < deadzone:
            return 0
        return val

    def teleopPeriodic(self):
        """
        What does this do?
        
        """
        """
        This function inverts the input from the stick for movement,
         and takes the input from the stick for rotation and sets them 
         equal to the forward movement speed and rotation speed respecively. 
         Then it calls a function to move the robot with the given parameters.
        """
        
        forward = -self.driver.getRawAxis(5)
        rotation_value = rotation_value = self.driver.getX(LEFT_HAND)
        
        forward = deadzone(forward, 0.2) #Safety

        self.myRobot.arcadeDrive(forward, rotation_value) #Actualy move

def deadzone(val, deadzone):
    """
    Square deadzone 
    """
    if abs(val) < deadzone:
        return 0
    elif val < (0):
        x = ((abs(val) - deadzone)/(1-deadzone))
        return (-x)
    else:
        x = ((val - deadzone)/(1-deadzone))
        return (x)

#  main entry point
if __name__ == "__main__":
  wpilib.run(MyRobot)
