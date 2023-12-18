from flask import Flask, request
from ROS import vehicle_odometry, offboard_control, camera_control
import rclpy
import os
import threading

app = Flask(__name__)
global offboard_control_instance

@app.route('/')
def hello():
    return '0'
    
@app.route('/get_position_x')
def get_postion_x():
    return vehicle_odometry.get_drone_pos_x()

@app.route('/get_position_y')
def get_postion_y():
    return vehicle_odometry.get_drone_pos_y()

@app.route('/shutdown_drone')
def shutdown_drone():
    if offboard_control_instance != None:
        offboard_control_instance.shutdown_drone = True
    return 'Shutting down drone'

global image_num
image_num = 1

@app.route('/take_image')
def take_image():
    global image_num
    distance = str(1.65 - offboard_control_instance.x)
    if image_num % 6 == 0:
        image_num = 1
    camera_control.take_image(distance,image_num)
    image_num += 1
    return "Image taken"


@app.route('/move_drone')
def move_drone():
    new_x = request.args.get('x')
    new_y = request.args.get('y')
    print(new_x,offboard_control_instance.x,new_y,offboard_control_instance.y)
    offboard_control_instance.x = float(new_x)
    offboard_control_instance.y = float(new_y)
    return 'moving drone along x axis'

def init_image_bridge():
    print("Starting image bridge...")
    def run_bridge():
        print("image bridge started...")
        os.system('ros2 run ros_gz_bridge parameter_bridge /camera@sensor_msgs/msg/Image@gz.msgs.Image')
    image_bridge_thread = threading.Thread(target=run_bridge)
    image_bridge_thread.start()

def init_rclpy():
    print("initializing rclpy")
    rclpy.init()

if __name__ == "__main__":
    init_rclpy()
    offboard_control_instance = offboard_control.OffboardControl()
    offboard_control.init(offboard_control_instance)
    init_image_bridge()
    app.run()

