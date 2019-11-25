import math
import ctre 
import wpilib
from wpilib import Ultrasonic
from wpilib import DoubleSolenoid
from navx import AHRS
from wpilib.interfaces import GenericHID
from wpilib.drive import DifferentialDrive

import robotpy_ext.common_drivers


#TODO: Check id's
#DRIVETRAIN IDs (talon and victor)
LEFT_MASTER_ID = 1
LEFT_SLAVE_1_ID = 2
LEFT_SLAVE_2_ID = 3

RIGHT_MASTER_ID = 4
RIGHT_SLAVE_1_ID = 5
RIGHT_SLAVE_2_ID = 6

#ELEVATOR ID (talon)
ELEVATOR_ID_MASTER = 7
ELEVATOR_ID_SLAVE = 8

#ELEVATOR PID IDs
MIN_ELEVATOR_RANGE = 0
MAX_ELEVATOR_RANGE = 200

#ELEVATOR STOPS in mm
LOW_HATCH_VALUE = 0
LOW_CARGO_VALUE = 500
MEDIUM_HATCH_VALUE = 800
MEDIUM_CARGO_VALUE = 1200
HIGH_HATCH_VALUE = MEDIUM_HATCH_VALUE
HIGH_CARGO_VALUE = MEDIUM_CARGO_VALUE


LEFT_CONTROLLER_HAND = wpilib.interfaces.GenericHID.Hand.kLeft
RIGHT_CONTROLLER_HAND = wpilib.interfaces.GenericHID.Hand.kRight

LEFT_HAND = GenericHID.Hand.kLeft
RIGHT_HAND = GenericHID.Hand.kRight

#BALL MANIPULATOR
BALL_MANIP_ID = 9
GATHER_SPEED = 1.0
SPIT_SPEED = -1.0
STOP_SPEED = 0.0

class Robot(wpilib.TimedRobot):
    def robotInit(self):
        #DRIVETRAIN
        self.left = createTalonAndSlaves(LEFT_MASTER_ID, LEFT_SLAVE_1_ID, LEFT_SLAVE_2_ID)
        self.right = createTalonAndSlaves(RIGHT_MASTER_ID, RIGHT_SLAVE_1_ID, RIGHT_SLAVE_2_ID)
        
        self.drivetrain = wpilib.drive.DifferentialDrive(self.left, self.right)

        self.controller = wpilib.XboxController(0) #TODO: get actual port of controller
        
        self.ballManipulator = BallManipulator(ctre.WPI_TalonSRX(BALL_MANIP_ID))


        #ELEVATOR
        elevator_motor = createTalonAndSlaves(ELEVATOR_ID_MASTER, ELEVATOR_ID_SLAVE)
        self.downSonar = None
        self.elevator = Elevator(elevator_motor, encoder_motor=elevator_motor)


    def robotPeriodic(self):
        return

    def teleopInit(self):
        print("TELEOP BEGINS")

    def teleopPeriodic(self):
        #TODO: figure out what values should be negative


        #Ball manipulator
        ballMotorSetPoint = 0

        if self.controller.getBumper(LEFT_HAND):
            ballMotorSetPoint = 1.0
        elif self.controller.getBumper(RIGHT_HAND):
            ballMotorSetPoint = -1.0
        else:
            ballMotorSetPoint = 0.0

        self.ballManipulator.set(ballMotorSetPoint)
        
        #Main Control
        forward = self.controller.getRawAxis(3)
        rotation_value = rotation_value = self.controller.getX(LEFT_HAND)
        
        forward = deadzone(forward, 0.2)

        self.drivetrain.arcadeDrive(forward, rotation_value)
        
        if self.controller.getAButton():
            forward = forward / 2
            rotation_value = rotation_value * 0.75
            
        #Elevator control
        left_trigger = self.controller.getTriggerAxis(LEFT_HAND)
        right_trigger = self.controller.getTriggerAxis(RIGHT_HAND)

        TRIGGER_LEVEL = 0.5

        #Up goes down, down goes up. It's a feature.
        if abs(left_trigger) > TRIGGER_LEVEL:
            self.elevator.go_up(0.5 * self.controller.getTriggerAxis(LEFT_HAND))
        elif abs(right_trigger) > TRIGGER_LEVEL:
            self.elevator.go_down(self.controller.getTriggerAxis(RIGHT_HAND))
        else:
            self.elevator.stop()

def createTalonAndSlaves(MASTER, slave1, slave2=None):
    '''
    First ID must be MASTER, Second ID must be slave TALON, Third ID must be slave VICTOR
    This assumes that the left and right sides are the same, two talons and one victor. A talon must be the master.
    '''
    master_talon = ctre.WPI_TalonSRX(MASTER)
    slave_talon = ctre.WPI_TalonSRX(slave1)
    slave_talon.follow(master_talon)
    
    if slave2 is not None:
        slave_talon2 = ctre.WPI_TalonSRX(slave2)
        slave_talon2.follow(master_talon)
    return master_talon

def deadzone(val, deadzone):
    if abs(val) < deadzone:
        return 0
    elif val < (0):
        x = ((abs(val) - deadzone)/(1-deadzone))
        return (-x)
    else:
        x = ((val - deadzone)/(1-deadzone))
        return (x)

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


class Elevator:
    def __init__(self, motor, encoder_motor=None):
        self.encoder_motor = encoder_motor
        self.motor = motor

    def go_up(self, speed = 1.0):
        self.motor.set(speed)

    def go_down(self, speed = 0.5):
        self.motor.set(-speed)

    def stop(self):
        self.motor.set(0)

    def set(self, setpoint):
        self.motor.set(setpoint)

if __name__ == "__main__":
	wpilib.run(Robot, physics_enabled = True)