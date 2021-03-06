#!/usr/bin/env python

import rospy
import sys
import pygazebo
import trollius
from trollius import From
from msg.gz_string_pb2 import GzString


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


if __name__ == '__main__':
    floor = rospy.myargv(argv=sys.argv)
    if len(floor) == 2:
        rospy.loginfo("Opening the elevator gate")
    else:
        rospy.logwarn("floor_num should be 0 or 1, but it contain: "
                      + str(len(floor)))
    loop = trollius.get_event_loop()
    loop.run_until_complete(setObject(floor[1]))
