#GENERAL PYTHON
import math
import time

#GENERAL ROBOT
import ctre 
import wpilib
from wpilib import Ultrasonic
from wpilib import DoubleSolenoid
from navx import AHRS
from wpilib.interfaces import GenericHID


import robotpy_ext.common_drivers

#OUR ROBOT SYSTEMS AND LIBRARIES
from subsystems.drivetrain import Drivetrain


LEFT_CONTROLLER_HAND = wpilib.interfaces.GenericHID.Hand.kLeft
RIGHT_CONTROLLER_HAND = wpilib.interfaces.GenericHID.Hand.kRight

#PCM CAN IDs
PCM_CAN_ID = 0

#DRIVETRAIN IDs (talon and victor)
LEFT_MASTER_ID = 1
LEFT_sub_unit_1_ID = 2
LEFT_sub_unit_2_ID = 3

RIGHT_MASTER_ID = 4
RIGHT_sub_unit_1_ID = 5
RIGHT_sub_unit_2_ID = 6





class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        #assigns driver as controller 0 and operator as controller 1
        self.driver = wpilib.XboxController(0)
        self.operator = wpilib.XboxController(1)
        #self.elevatorController = ElevatorController(self.operator, self.logger)

        #GYRO
        self.gyro = AHRS.create_spi()

        #DRIVETRAIN
        left = createTalonAndsub_units(LEFT_MASTER_ID, LEFT_sub_unit_1_ID, LEFT_sub_unit_2_ID)
        right = createTalonAndsub_units(RIGHT_MASTER_ID, RIGHT_sub_unit_1_ID, RIGHT_sub_unit_2_ID)
        self.drivetrain = Drivetrain(left, right, self.gyro)

    

        self.autoBalancing = False

    def robotPeriodic(self):
        # if self.timer % 50 == 0:
        #     print("NavX Gyro Roll", self.gyro.getRoll())
        pass

    def teleopInit(self):
        """Executed at the start of teleop mode"""
        self.forward = 0
        
        
    def teleopPeriodic(self):
        deadzone_value = 0.2
        max_accel = 0.15
        max_forward = 1.0
        max_rotate = 1.0

        goal_forward = -self.driver.getRawAxis(5)

        rotation_value = self.driver.getX(LEFT_CONTROLLER_HAND)
        
        goal_forward = deadzone(goal_forward, deadzone_value) * max_forward

        delta = goal_forward - self.forward

        
        if(self.driver.getRawAxis(5) < 0):
            self.forward = 0
        else:
            self.forward += delta
        
        self.drivetrain.arcade_drive(self.forward, rotation_value) 


    def autonomousInit(self):
        #Because we want to drive during auton, just call the teleopInit() function to 
        #get everything from teleop.
        self.teleopInit()
        print("auton init")

    def autonomousPeriodic(self):
        self.teleopPeriodic()
        print("auton periodic")

def createTalonAndsub_units(MASTER, sub_unit1, sub_unit2=None):
    '''
    First ID must be MASTER, Second ID must be sub_unit TALON, Third ID must be sub_unit VICTOR
    This assumes that the left and right sides are the same, two talons and one victor. A talon must be the master.
    '''
    master_talon = ctre.WPI_TalonSRX(MASTER)
    sub_unit_talon = ctre.WPI_TalonSRX(sub_unit1)
    sub_unit_talon.follow(master_talon)
    
    if sub_unit2 is not None:
        sub_unit_talon2 = ctre.WPI_TalonSRX(sub_unit2)
        sub_unit_talon2.follow(master_talon)
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

def sign(number):
    if number > 0:
        return 1
    else:
        return -1
        
if __name__ == "__main__":
    wpilib.run(MyRobot)

