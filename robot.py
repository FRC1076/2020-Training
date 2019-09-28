import wpilib
import ctre
from wpilib.drive import DifferentialDrive
from wpilib.interfaces import GenericHID
import robot_values

#MOTOR PORTS
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
        """Robot initialization function"""
        # object that handles basic drive operations
        self.leftVictor = ctre.WPI_VictorSPX(LEFT)
        self.rightVictor = ctre.WPI_VictorSPX(RIGHT)
        self.centerVictor1 = ctre.WPI_VictorSPX(CENTER1)
        self.centerVictor2 = ctre.WPI_VictorSPX(CENTER2)

        self.left = wpilib.SpeedControllerGroup(self.leftVictor)
        self.right = wpilib.SpeedControllerGroup(self.rightVictor)

        self.center1 = wpilib.SpeedControllerGroup(self.centerVictor1)
        self.center2 = wpilib.SpeedControllerGroup(self.centerVictor2)

        self.myRobot = DifferentialDrive(self.left, self.right)
        self.myRobot.setExpiration(0.1)

        # joysticks 1 & 2 on the driver station
        # self.leftStick = wpilib.Joystick(0)
        # self.rightStick = wpilib.Joystick(1)

        self.DEADZONE = 0.4

        self.LEFT = GenericHID.Hand.kLeft
        self.RIGHT = GenericHID.Hand.kRight

        self.driver = wpilib.XboxController(0)

        self.ballManipulator = BallManipulator(ctre.WPI_VictorSPX(BALL_MANIP_ID))

    def autonomousInit(self):
        self.myRobot.tankDrive(0.8, 0.8)

    def autonomousPeriodic(self):
        self.myRobot.tankDrive(1, 0.5)

    def teleopInit(self):
        """Executed at the start of teleop mode"""
        self.myRobot.setSafetyEnabled(True)

    def setCenters(self, speed_value):
        self.center1.set(-speed_value)
        self.center2.set(speed_value)

    def deadzone(self, val, deadzone):
        if abs(val) < deadzone:
            return 0
        return val

    def teleopPeriodic(self):
        ballMotorSetPoint = 0

        if self.driver.getBumper(self.LEFT):
            ballMotorSetPoint = 1.0
        elif self.driver.getBumper(self.RIGHT):
            ballMotorSetPoint = -1.0
        else:
            ballMotorSetPoint = 0.0

        self.ballManipulator.set(ballMotorSetPoint)

        """Runs the motors with tank steering"""
        #right = self.driver.getY(self.RIGHT)
        #left = self.driver.getY(self.LEFT)

        #self.myRobot.tankDrive(right, left)
        forward = -self.driver.getRawAxis(5) * robot_values.DRIVE_SPEED
        rotation_value = rotation_value = self.driver.getX(LEFT_HAND)
        
        forward = deadzone(forward, robot_values.DEADZONE)

        self.myRobot.arcadeDrive(forward, rotation_value)


        center_speed = self.driver.getX(self.RIGHT)

        self.setCenters(self.deadzone(center_speed, self.DEADZONE))

class BallManipulator:
    """
    Manipulator wraps a motor controller that gathers and spits
    out the cargo balls.
    """
    def __init__(self, motor):
        self.motor = motor

    def gather(self, speed = GATHER_SPEED):
        self.motor.set(speed)

    def spit(self, speed = SPIT_SPEED):
        self.motor.set(speed)

    def stop(self):
        self.motor.set(STOP_SPEED)

    def set(self, setValue):
        """
        Direct control to be used with a controller
        that puts out f, 0, and -f for gather, stop,
        and spit, respectively.
        """
        self.motor.set(setValue)

def deadzone(val, deadzone):
    if abs(val) < deadzone:
        return 0
    elif val < (0):
        x = ((abs(val) - deadzone)/(1-deadzone))
        return (-x)
    else:
        x = ((val - deadzone)/(1-deadzone))
        return (x)

if __name__ == "__main__":
    wpilib.run(MyRobot)