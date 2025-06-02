# ranger-ws
ros2 topic descriptions: 

# /actuator_state
Type: ranger_msgs/msg/ActuatorStateArray

Example message: 

- id: 7
  motor:
    rpm: 0
    current: 0.0
    pulse_count: 0
  driver:
    driver_voltage: 49.20000076293945
    driver_temperature: 28.0
    motor_temperature: 26.0
    driver_state: 0


 where No. 0 is the right front wheel motor, No. 1 is the right rear wheel motor, No. 2 is the left rear wheel motor, No. 3 is the left front wheel motor, No. 4 is the right front steering motor, No. 5 is the right rear steering motor, No. 6 is the left rearsteering motor, and No. 7 is the left front steering motor.

 # /battery_state
 Type: sensor_msgs/msg/BatteryState

 Example message: 

 header:
   stamp:
     sec: 1748899754
     nanosec: 526543712
   frame_id: ''
 voltage: 498.0
 temperature: 25.100000381469727
 current: -0.30000001192092896
 charge: .nan
 capacity: .nan
 design_capacity: .nan
 percentage: 96.0
 power_supply_status: 0
 power_supply_health: 0
 power_supply_technology: 2
 present: false
 cell_voltage: []
 cell_temperature: []
 location: ''
 serial_number: ''

# /motion_state
Type: ranger_msgs/msg/MotionState

Example message:

header:
  stamp:
    sec: 1748899958
    nanosec: 958790685
  frame_id: ''
motion_mode: 3

where motion_mode = 0 means the robot is in dual ackermann steering mode, motion_mode = 1 means the robot's wheels are parallel, motion_mode = 2 means the robot is in spinning mode, motion_mode = 3 means the robot is parked, motion_mode = 4 means the robot is in side slip mode. 


# /rc_state
Type: ranger_msgs/msg/RCState

Example message: 

swa: 0
swb: 2
swc: 1
swd: 0
stick_right_v: 0
stick_right_h: 0
stick_left_v: 0
stick_left_h: 0
var_a: 0

The state of controller switches and joysticks.

# /system_state
Type: ranger_msgs/msg/SystemState

Example message: 

header:
  stamp:
    sec: 1748900279
    nanosec: 918745888
  frame_id: ''
vehicle_state: 0
control_mode: 1
error_code: 0
battery_voltage: 50.900001525878906
motion_mode: 0

where
```
uint8 VEHICLE_STATE_NORMAL = 0
uint8 VEHICLE_STATE_ESTOP = 1
uint8 VEHICLE_STATE_EXCEPTION = 2

uint8 CONTROL_MODE_RC = 0
uint8 CONTROL_MODE_CAN = 1
```


