# define variables
marker_3_count = 1
marker_func_list = [None,marker_1,marker_2,marker_3,marker_4,marker_5]
end = False

def get_marker():
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)

    while True:
        # Get marker detection info
        marker_info = vision_ctrl.get_marker_detection_info()
        # Check if any markers are detected
        if marker_info[0] == 1:
            marker_id = marker_info[1 + i * 6]
            vision_ctrl.disable_detection(rm_define.vision_detection_marker)
            return marker_id - 10
        # Error seeing multiple markers

        else: 
            print('No marker detected')
        time.sleep(0.1)
    
def align_to_marker(target_marker_id):

    #FOV = 120

    vision_ctrl.enable_detection(rm_define.vision_detection_marker)
    for i in range(2):
        while True:

            print("marker_align")

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
                        move_x = 1 if dx > 0 else -1  # Move right if marker is right of center, and vice versa
                        #move_y = -1 if dy > 0 else 1  # Move forward if marker is below center, and vice versa

                        # Adjust speeds for fine-tuning the position

                        speed_x = abs(dx)*4
                        #if speed_x > 1:
                            #speed_x = 1

                        #speed_x = min(1, abs(dx) * 2)  # Scale speed based on distance from center
                        #speed_y = min(1, abs(dy) * 2)  # Scale speed based on distance from center

                        # Move the robot to center the marker                                                                                         
                        if abs(dx) > 0.02:  # Only move if the deviation is significant
                            chassis_ctrl.set_trans_speed(speed_x)
                            chassis_ctrl.move(90 * move_x)  # Move horizontally

                            print(90 * move_x)

                        #elif abs(dy) > 0.05:  # Only move if the deviation is significant
                        #    chassis_ctrl.set_trans_speed(speed_y)
                        #    chassis_ctrl.move_with_time(0, 0.1)  # Move forward/backward
                        # Check if the marker is centered
                        if abs(dx) <= 0.02: #and abs(dy) <= 0.05:
                            chassis_ctrl.stop()
                            print(f"Marker {target_marker_id} centered at ({x})")
                            return
            
            # Sleep for a short while to avoid overwhelming the processor
            time.sleep(0.1)
        

    vision_ctrl.disable_detection(rm_define.vision_detection_marker)

def move_to_object(gap):
    ir_distance_sensor_ctrl.enable_measure(1)
    time.sleep(0.5)
    dist = ir_distance_sensor_ctrl.get_distance_info(1)
    print(dist)
    chassis_ctrl.move_with_distance(0,(dist - gap)/110)

#recs = 0
def moveUntil_IRdetect(safe_distance):

        #recs += 1
        print("recs:")

        ir_distance_sensor_ctrl.enable_measure(1)

        chassis_ctrl.move(0)

        ir_distance_sensor_ctrl.cond_wait('ir_distance_1_lt_' + str(safe_distance))

        #while ir_distance_sensor_ctrl.get_distance_info(1) > safe_distance:
            ##time.sleep(0.01)
    
        chassis_ctrl.stop()

        ir_distance_sensor_ctrl.disable_measure(1)

        chassis_ctrl.set_trans_speed(0.2)
        chassis_ctrl.move_with_distance(0,safe_distance/100 * 0.5)

        #time.sleep(1)
        ir_distance_sensor_ctrl.disable_measure(1)
        print("complete")

def reset_to_marker(marker_number, gap):
    align_to_marker(marker_number)
    #move_to_object(gap)
    moveUntil_IRdetect(gap)

def marker_distance()
    marker_dist = 0.5
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)
    vision_ctrl.set_marker_detection_distance(marker_dist)

    marker_seen = False
    while True:
        # Get marker detection info
        marker_info = vision_ctrl.get_marker_detection_info()
    
        # Check if any markers are detected
        if marker_info[0] > 0:
            print(f'Marker is {marker_dist} away')
            marker_seen = True
            return marker_dist
            break
        #increases possible marker distance range
        else:
            marker_dist += 0.05

            #upper limit of camera range
            if marker_dist > 4:
                print('Error. Marker not seen')
                marker_distance = 3
            #Change detection distance
            vision_ctrl.set_marker_detection_distance(marker_dist)
            # Sleep for a short while to avoid overwhelming the processor
            time.sleep(0.1)

def reset_to_marker_w_camera(marker_number, gap):
    align_to_marker(marker_number)
    dist = marker_distance()
    chassis_ctrl.move_with_distance(0,(dist - gap)/100)


def marker_1():

    #robotic_arm_ctrl.recenter()

    #print("m1 init")

    #try:
    #    print(dir(chassis_ctrl))
    #except:
    #    print("dir unsucc") #oop unaccessible

    rotate_speed = 90
    move_speed = 1
    safe_distance = 50

    chassis_ctrl.set_rotate_speed(rotate_speed)
    chassis_ctrl.set_trans_speed(move_speed)


    #move forward until wall
    
    moveUntil_IRdetect(safe_distance)
    chassis_ctrl.set_trans_speed(move_speed)

    # turn right 90 degrees
    
    chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90)

    # go to turn
    moveUntil_IRdetect(safe_distance)
    chassis_ctrl.set_trans_speed(move_speed)
    
    #turn 90 left
    chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)

    #move until hit

    moveUntil_IRdetect(safe_distance)
    chassis_ctrl.set_trans_speed(move_speed)

    #turn 90 left
    chassis_ctrl.rotate_with_degree(rm_define.anticlockwise, 90)

    chassis_ctrl.move_with_distance(90, 0.2)

    #in front

    moveUntil_IRdetect(safe_distance)
    chassis_ctrl.set_trans_speed(move_speed)

    #turn 90 right
    chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90)

    print("m1 finish")

    return

def marker_2():
    reset_to_marker(12,10)
    #robot is at H3 and facing H3

    #move to turn
    chassis_ctrl.set_trans_speed(1)
    chassis_ctrl.move_with_distance(90,1.3)
    chassis_ctrl.stop()

    #face door
    chassis_ctrl.set_rotate_speed(45)
    chassis_ctrl.rotate_with_degree(rm_define.clockwise, 180)
    chassis_ctrl.stop()

    #keep moving until against door

    moveUntil_IRdetect(20)

    #wait for gunner to shoot target
    time.sleep(5)
    #cross gate
    chassis_ctrl.move_with_distance(0, 0.5)
    return

def marker_3():    
    if marker_3_count == 1:
        reset_to_marker(13,10)
        #Grabs cone
        robotic_arm_ctrl.moveto(0,0,wait_for_complete=True)
        gripper_ctrl.update_power_level(3)
        gripper_ctrl.close()
        time.sleep(2)
        robotic_arm_ctrl.recenter()

        chassis_ctrl.set_rotate_speed(90)
        #Move to the next marker
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise,180)
        # moveUntil_IRdetect(10)

        # ir_distance_sensor_ctrl.cond_wait('ir_distance_1_gt_30')
            
        # moveUntil_IRdetect(10)
        # chassis_ctrl.rotate_with_degree(rm_define.clockwise,90)
        
        # chassis_ctrl.set_trans_speed(0.5)

        # chassis_ctrl.move_with_distance(180, 0.2)
        # #time.sleep(2/5)
        # chassis_ctrl.rotate_with_degree(rm_define.clockwise, 180)
        # #time.sleep(180/90)
        
        #wait for door to open
        time.sleep(3)

        chassis_ctrl.move_with_distance(0, 3)
        #time.sleep(1.5/0.5)
        chassis_ctrl.rotate_with_degree(rm_define.clockwise, 90)
        #time.sleep(1)

        #increase count for next marker 3
        marker_3_count += 1

    elif marker_3_count == 2:
        #Move to drop point
        reset_to_marker_w_camera(13,15)
        chassis_ctrl.rotate_with_degree(rm_define.anticlockwise,90)
        chassis_ctrl.move_with_distance(0,0.1)
        #Drop cone
        gripper_ctrl.open()
        sleep(3)
        #Move back to marker
        chassis_ctrl.move_with_distance(180,0.1)

        gripper_ctrl.recenter()

        chassis_ctrl.rotate_with_degree(rm_define.clockwise,180)
        #move closer to marker 5
        chassis_ctrl.move_with_distance(0,1)

    
def marker_4(): # S turn, no stop

    reset_to_marker_w_camera(14,15)

    chassis_ctrl.set_trans_speed(0.5)
    chassis_ctrl.set_rotate_speed(90)

    chassis_ctrl.move_with_distance(0, 1.3)
    #time.sleep(1.3/0.5)
    chassis_ctrl.rotate_with_degree(rm_define.clockwise,135)
    #time.sleep(135/90)
    chassis_ctrl.move_with_distance(0, 1.3)
    #time.sleep(1.3/0.5)
    chassis_ctrl.rotate_with_degree(rm_define.anticlockwise,135)
    #time.sleep(135/90)

    chassis_ctrl.move_with_distance(0,1)
    #time.sleep(2)

    return

def marker_5():

    align_to_marker(15)

    moveUntil_IRdetect(10)

    chassis_ctrl.set_trans_speed(0.5)
    chassis_ctrl.move_with_distance(90,1.3)
    #time.sleep(1.3)

    chassis_ctrl.move(0)
    vision_ctrl.enable_detection(rm_define.vision_detection_marker)
    vision_ctrl.cond_wait(rm_define.cond_recognized_marker_trans_red_heart)

    chassis_ctrl.stop()
    vision_ctrl.disable_detection(rm_define.vision_detection_marker)
    moveUntil_IRdetect(10)
    end = True
    #completed
    print("Completed execution! Hooray")


def start():

    while True:

        marker_number = get_marker()
        print(f"marker number: {marker_number}")
        marker_func_list[marker_number]()
        if end == True:
            break