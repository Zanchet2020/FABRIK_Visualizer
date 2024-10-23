import math
from typing import List

class Joint:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class Connection:
    def __init__(self, a: int, b: int, d: float):
        self.a = a
        self.b = b
        self.distance = d



class Body:
    def __init__(self, joints):
        self.joints = []
        self.connections = []
        for i in range(len(joints)):
            joint = Joint(joints[i][0], joints[i][1])
            self.joints.append(joint)
            if i == 0:
                self.origin = (joints[0][0], joints[0][1])
                continue
            dx = joints[i][0] - joints[i-1][0]
            dy = joints[i][1] - joints[i-1][1]
            d = math.sqrt(dx * dx + dy * dy)
            conn = Connection(i-1, i, d)
            self.connections.append(conn)
            
    def reach(self, x, y):    
        for i in range(10):
            forward_reach(x, y)
            backward_reach(self.origin[0], self.origin[1])
            
            
    def forward_reach(x, y):
        dx = x - self.origin[0]
        dy = y - self.origin[1]
        dist = sqrt(dx * dx + dy * dy)
        body_length = sum(c.distance for c in body.connections)

        if dist > body_lenght:
            for joint in self.joints:
        

    def backward_reach(x, y):
