import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.conditions import IfCondition


def generate_launch_description():
	pkg_rm3_nav = get_package_share_directory('nav_rm3')
	pkg_nav2_bringup = get_package_share_directory('nav2_bringup')
	namespace = LaunchConfiguration('namespace', default='')
	use_sim_time = LaunchConfiguration('use_sim_time', default='true')
	with_rviz = LaunchConfiguration('with_rviz', default='true')
	nav2_config_file = LaunchConfiguration('params', 
						default=os.path.join(pkg_rm3_nav, 'config', 'nav2_params.yaml'))
	rviz_config_file = LaunchConfiguration('rviz_config',
						default=os.path.join(pkg_nav2_bringup, 'rviz', 'nav2_default_view.rviz'))

	# nav2 bringup launch file
	nav2_bringup_launch_file = IncludeLaunchDescription(
					PythonLaunchDescriptionSource(os.path.join(pkg_nav2_bringup, 'launch', 'navigation_launch.py')),
					launch_arguments={
						'use_sim_time': use_sim_time,
						'params_file': nav2_config_file,
						'namespace': namespace,
                              		'use_lifecycle_mgr': 'false',
                              		'map_subscribe_transient_local': 'true'}.items(),
					)

	# rviz2
	rviz2 = Node(package='rviz2', executable='rviz2',
					name='rviz2',
					arguments=['-d', rviz_config_file],
					parameters=[{'use_sim_time': use_sim_time}],
					output='screen',
					condition=IfCondition(with_rviz))
					

	
	return LaunchDescription([
		DeclareLaunchArgument('namespace',
       		 	default_value='',
        			description='Top-level namespace'),
		DeclareLaunchArgument('params_file',
		     		default_value=nav2_config_file,
		     		description="Path to nav2 config file"),
		DeclareLaunchArgument('use_sim_time',
                                default_value=use_sim_time,
                                description="Use sim clock or not"),
		DeclareLaunchArgument('with_rviz',
								default_value=with_rviz,
								description='Launch rviz2'),
		nav2_bringup_launch_file,
		rviz2
		])
