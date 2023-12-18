from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import rclpy
import cv2
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
bridge = CvBridge()

class ImageListener(Node):
    """Node for controlling a vehicle in offboard mode."""
    x = 0.0
    y = 0.0
    def __init__(self) -> None:
        super().__init__('vehicle_odom')
        # Configure QoS profile for publishing and subscribing
        qos_profile = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=1
        )   
        # Create subscribers
        self.image_subscriber = self.create_subscription(
            Image, '/camera', self.image_callback, qos_profile)
    def image_callback(self, msg):
        print("Received an image!")
        try:
            # Convert your ROS Image message to OpenCV2
            cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            print(e)
        else:
            # Save your OpenCV2 image as a jpeg 
            cv2.imwrite('camera_image.jpeg', cv2_img)
            self.destroy_node()

    
def take_image():
    executor = rclpy.executors.SingleThreadedExecutor()
    image_listener = ImageListener()
    executor.add_node(image_listener)
    executor.spin_once()
    return "took image"