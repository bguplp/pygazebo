#!/usr/bin/env python

import rospy
import pygazebo
import trollius
from trollius import From
from msg.gz_string_pb2 import GzString
from pygazebo_ros_gazebo_elevator.srv import CallElevator, CallElevatorResponse


@trollius.coroutine
def setObject(floor):
    manager = yield From(pygazebo.connect())
    publisher = yield From(
        manager.advertise('/gazebo/default/elevator',
                          'gazebo.msgs.GzString'))
    msg = GzString()
    msg.data = str(floor)
    for _ in xrange(3):
        yield From(publisher.publish(msg))
        yield From(trollius.sleep(1.0))


def callback_function(req):
    res = "false"
    loop = trollius.new_event_loop()
    trollius.set_event_loop(loop)
    loop.run_until_complete(setObject(req.floor_num))
    res = "true"
    return CallElevatorResponse(res)


if __name__ == '__main__':
    rospy.init_node("call_elevator_node", anonymous=True)
    rospy.Service("call_elevator", CallElevator, callback_function)
    rospy.loginfo("Call elevator service, waiting for request")
    rospy.spin()
