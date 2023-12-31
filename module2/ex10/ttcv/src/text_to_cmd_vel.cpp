#include <chrono>
#include <memory>
#include <map>


#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "geometry_msgs/msg/twist.hpp"
using std::placeholders::_1;

class TextCmd : public rclcpp::Node
{
public:	

	TextCmd() : Node("text_to_cmd_vel")
	{
		cmdVel_pub = this->create_publisher<geometry_msgs::msg::Twist>("/turtle1/cmd_vel", 10);
		text_pub = this->create_subscription<std_msgs::msg::String>("/cmd_text", 10, std::bind(&TextCmd::text_to_cmd, this, _1));
	}
private:
	rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr cmdVel_pub;
	rclcpp::Subscription<std_msgs::msg::String>::SharedPtr text_pub;

	//gets a string as input, publishes Twist
	void text_to_cmd(const std_msgs::msg::String &msg) const
	{
		geometry_msgs::msg::Twist twist;
		RCLCPP_INFO(this->get_logger(), "I heard %s", msg.data.c_str());
		
		if (msg.data == "turn_left") { twist.angular.z = -1.4; twist.linear.x = 1; }
		if (msg.data == "turn_right") { twist.angular.z = 1.4; twist.linear.x = 1; }
		if (msg.data == "move_backward") twist.linear.x = -1;		
		if (msg.data == "move_forward") twist.linear.x = 1;		

		RCLCPP_INFO(this->get_logger(), "I know twist linear %f and twist angular %f", twist.linear.x, twist.angular.z);
		
		cmdVel_pub->publish(twist);
	}

};


int main(int argc, char* argv[])
{
	rclcpp::init(argc, argv);
	rclcpp::spin(std::make_shared<TextCmd>());
	rclcpp::shutdown();
	return 0;
}
