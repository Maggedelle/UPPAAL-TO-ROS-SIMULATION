from flask import Flask
from ROS import vehicle_odometry
app = Flask(__name__)

@app.route('/')
def hello():
    return '0'
    
@app.route('/get_position_x')
def get_postion_x():
    return vehicle_odometry.get_drone_state()


if __name__ == "__main__":
    vehicle_odometry.init_rclpy()
    app.run(debug=True)

