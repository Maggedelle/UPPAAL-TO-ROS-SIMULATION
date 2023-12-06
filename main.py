from flask import Flask
from ROS import vehicle_odometry, offboard_control
import rclpy

app = Flask(__name__)
global offboard_control_instance


@app.route('/')
def hello():
    return '0'
    
@app.route('/get_position_x')
def get_postion_x():
    return vehicle_odometry.get_drone_state()

@app.route('/shutdown_drone')
def shutdown_drone():
    if offboard_control_instance != None:
        offboard_control_instance.shutdown_drone = True
    return 'Shutting down drone'


@app.route('/move_drone_along_x_axis')
def move_along_x_axis():
    offboard_control_instance.x -= 0.1
    print(offboard_control_instance.x)
    return 'moving drone along x axis'


def init_rclpy():
    print("initializing rclpy")
    rclpy.init()

if __name__ == "__main__":
    init_rclpy()
    offboard_control_instance = offboard_control.OffboardControl()
    offboard_control.init(offboard_control_instance)
    app.run()

