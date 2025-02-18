#!/usr/bin/python3
"""
Copyright (c) 2012,
Systems, Robotics and Vision Group
University of the Balearican Islands
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of Systems, Robotics and Vision Group, University of
      the Balearican Islands nor the names of its contributors may be used to
      endorse or promote products derived from this software without specific
      prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


PKG = 'bag_tools' # this package name

import roslib; roslib.load_manifest(PKG)
import rospy
import rosbag
import os
import sys
import argparse

def extract_topics(inbag, outbag, topics):
    rospy.loginfo('   Processing input bagfile: %s', inbag)
    rospy.loginfo('  Writing to output bagfile: %s', outbag)
    rospy.loginfo('          Extracting topics: %s', topics)

    outbag = rosbag.Bag(outbag,'w')
    
    total_messages = rosbag.Bag(inbag,'r').get_message_count()
    processed_messages = 0
    
    for topic, msg, t in rosbag.Bag(inbag,'r').read_messages():
        try:
            if topic in topics:
                outbag.write(topic, msg, t)
                processed_messages += 1
                if processed_messages % 10 == 0:
                    rospy.loginfo('Processed %s out of %s messages...', processed_messages, total_messages)
        except Exception as e:
            rospy.logerr('Error processing message from topic %s at time %s', topic, t)
            rospy.logerr(str(e))
    rospy.loginfo('Closing output bagfile and exit...')
    outbag.close();


if __name__ == "__main__":
    rospy.init_node('extract_topics')
    parser = argparse.ArgumentParser(
        description='Extracts topics from a bagfile into another bagfile.')
    parser.add_argument('inbag', help='input bagfile')
    parser.add_argument('outbag', help='output bagfile')
    parser.add_argument('topics', nargs='+', help='topics to extract')
    args = parser.parse_args()

    try:
        extract_topics(args.inbag,args.outbag,args.topics)
    except Exception as e:
        import traceback
        traceback.print_exc()

