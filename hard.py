# define variables
marker_3_count = 0

def get_marker():
    pass
    
def align_to_marker(target_marker_id):
    while True:
        # Get marker detection info
        marker_info = vision_ctrl.get_marker_detection_info()
        
        # Check if any markers are detected
        if marker_info[0] > 0:
            # Loop through the detected markers
            num_markers = marker_info[0]
            for i in range(num_markers):
                # Extract the ID of each detected marker
                marker_id = marker_info[1 + i * 6]
                
                # Check if this is the target marker
                if marker_id == target_marker_id:
                    # Extract the coordinates of the marker
                    x = marker_info[2 + i * 6]
                    #y = marker_info[3 + i * 6]

                    # Calculate the difference from the center
                    dx = x - 0.5
                    #dy = y - 0.5

                    # Determine the movement directions
                    move_x = 1 if dx > 0 else 1  # Move right if marker is right of center, and vice versa
                    #move_y = -1 if dy > 0 else 1  # Move forward if marker is below center, and vice versa

                    # Adjust speeds for fine-tuning the position
                    speed_x = min(1, abs(dx) * 2)  # Scale speed based on distance from center
                    #speed_y = min(1, abs(dy) * 2)  # Scale speed based on distance from center

                    # Move the robot to center the marker                                                                                         
                    if abs(dx) > 0.05:  # Only move if the deviation is significant
                        chassis_ctrl.set_trans_speed(speed_x)
                        chassis_ctrl.move_with_time(90 * move_x, 0.1)  # Move horizontally

                    #elif abs(dy) > 0.05:  # Only move if the deviation is significant
                    #    chassis_ctrl.set_trans_speed(speed_y)
                    #    chassis_ctrl.move_with_time(0, 0.1)  # Move forward/backward
                    # Check if the marker is centered
                    if abs(dx) <= 0.05: #and abs(dy) <= 0.05:
                        print(f"Marker {target_marker_id} centered at ({x})")
                        return
        
        # Sleep for a short while to avoid overwhelming the processor
        time.sleep(0.1)

def move_to_object(gap):
    ir_distance_sensor_ctrl.enable_measure(1)
    dist = ir_distance_sensor_ctrl.get_distance_info(1)
    chassis_ctrl.move_with_distance(0,dist - gap)

def reset_to_marker(marker_number, gap):
    align_to_marker(marker_number)
    move_to_object(gap)

def marker_1():

    rotate_speed = 90
    safe_distance = 5
    chassis_ctrl.set_rotate_speed(rotate_speed)

    #move forward until 10cm from wall

    chassis_ctrl.set_trans_speed(1)
    ir_distance_sensor_ctrl.enable_measure(1)

    chassis_ctrl.move(0)

    while ir_distance_sensor_ctrl.get_distance_info(1) > safe_distance:
        time.sleep(0.01)
    
    chassis_ctrl.stop()

    # turn right 90 degrees
    
    chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90)
    time.sleep(90/rotate_speed)
    chassis_ctrl.stop()

    # go to turn
    chassis_ctrl.set_trans_speed(2)
    chassis_ctrl.move(0)

    while ir_distance_sensor_ctrl.get_distance_info() > safe_distance:
        time.sleep(0.01)

    chassis_ctrl.stop()
    
    #turn 90 left
    chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)
    time.sleep(90/rotate_speed)

    #move until hit

    chassis_ctrl.set_trans_speed(2)
    chassis_ctrl.move(0)

    while ir_distance_sensor_ctrl.get_distance_info() > safe_distance:
        time.sleep(0.01)

    chassis_ctrl.stop()

    #turn and face
    chassis_ctrl.set_trans_speed(1)
    chassis_ctrl.move(0)

    while ir_distance_sensor_ctrl.get_distance_info() > safe_distance:
        time.sleep(0.01)

    chassis_ctrl.stop()

    #turn back
    chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90)
    time.speed(90/rotate_speed)

    #go until wall

    chassis_ctrl.set_trans_speed(2)
    chassis_ctrl.move(0)

    while ir_distance_sensor_ctrl.get_distance_info() > safe_distance:
        time.sleep(0.01)

    chassis_ctrl.stop()

    # turn to face H3
    chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90)
    time.sleep(90/rotate_speed)

    return

def marker_2():

    #robot is at H3 and facing H3

    #move to turn
    chassis_ctrl.set_trans_speed(2)
    chassis_ctrl.move_with_distance(90,1.3)
    time.sleep(1.3/2)
    chassis_ctrl.stop()

    #face door
    chassis_ctrl.set_rotate_speed(45)
    chassis_ctrl.rotate_with_degree(rm_define.clockwise, 180)
    time.sleep(180/45)
    chassis_ctrl.stop()

    #keep moving until against door
    ir_distance_sensor_ctrl.enable_measure(1)

    chassis_ctrl.move(0)
    while ir_distance_sensor_ctrl.get_distance_info(1) > 10:
        time.sleep(0.05)
    chassis_ctrl.stop()

    #wait for gunner to shoot target
    #time.sleep(5)

    while ir_distance_sensor_ctrl.get_distance_info(i) > 10:
        time.sleep(0.25)
    ir_distance_sensor_ctrl.disable_measure(1)

    #Cross gate

    chassis_ctrl.move_with_distance(0,0.8)
    time.sleep(0.8/2)
    chassis_ctrl.stop()

    return

def marker_3(count):
    reset_to_marker()
    if count == 1:
        #Grabs cone
        robotic_arm_ctrl.moveto(0,0,wait_for_complete=True)
        gripper_ctrl.update_power_level(3)
        gripper_ctrl.close()
        sleep(3)
        robotic_arm_ctrl.recenter()


        #Move to the next marker
        chassis_ctrl.rotate_with_time(rm_define.anticlockwise,6)
        move_to_object(10)

        while True: 
            if ir_distance_sensor_ctrl.get_distance_info(1) > 30:
                break
            sleep(0.1)
        move_to_object(10)
        chassis_ctrl.rotate_with_time(rm_define.clockwise,3)
        

    elif count == 2:
        #Move to drop point
        chassis_ctrl.rotate_with_time(rm_define.anticlockwise,3)
        chassis_ctrl.move_with_distance(0,0)
        #Drop cone
        gripper_ctrl.open()
        sleep(3)
        #Move back to marker
        chassis_ctrl.move_with_distance(0,0)
        chassis_ctrl.rotate_with_time(rm_define.clockwise,6)
    
def marker_4(): # S turn, no stop

    chassis_ctrl.set_trans_speed(1)

    chassis_ctrl.set_rotate_speed(90)

    chassis_ctrl.move(0)
    chassis_ctrl.rotate_with_degree(rm_define.clockwise, 180)

    time.sleep(2)

    chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 180)

    time.sleep(2)

    chassis_ctrl.stop()

    return

def start():

    for i in range(2):
        marker_1()

    marker_2()

    #insert while true loop, break when marker is detected

    marker_3(marker_3_count)

    marker_4()
