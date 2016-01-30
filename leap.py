import sys
if sys.platform == "darwin":
    import OSX.Leap as Leap
    import OSX.Mouse as Mouse
    from OSX.Leap import \
        Arm, Bone, Finger, Tool, Hand, Gesture, Screen, Device, Image, Mask, \
        CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture, \
        PointableList, FingerList, ToolList, HandList, MaskList, ScreenList, DeviceList, ImageList, \
        TrackedQuad, InteractionBox, Frame, Config, Controller, Listener
elif 'linux' in sys.platform:
    import Linux.Leap as Leap
    import Linux.Mouse as Mouse
    from Linux.Leap import \
        Arm, Bone, Finger, Tool, Hand, Gesture, Screen, Device, Image, Mask, \
        CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture, \
        PointableList, FingerList, ToolList, HandList, MaskList, ScreenList, DeviceList, ImageList, \
        TrackedQuad, InteractionBox, Frame, Config, Controller, Listener
else:
    import Windows.Leap as Leap
    import Windows.Mouse as Mouse
    from Windows.Leap import \
        Arm, Bone, Finger, Tool, Hand, Gesture, Screen, Device, Image, Mask, \
        CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture, \
        PointableList, FingerList, ToolList, HandList, MaskList, ScreenList, DeviceList, ImageList, \
        TrackedQuad, InteractionBox, Frame, Config, Controller, Listener

