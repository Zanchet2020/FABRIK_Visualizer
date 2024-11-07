import math
from typing import List
import time

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
    def __init__(self, jts):
        self.joints = []
        self.connections = []
        for i in range(len(jts)):
            joint = Joint(jts[i][0], jts[i][1])
            self.joints.append(joint)
            if i == 0:
                self.origin = joint
                continue
            dx = jts[i][0] - jts[i-1][0]
            dy = jts[i][1] - jts[i-1][1]
            d = math.sqrt(dx * dx + dy * dy)
            conn = Connection(i-1, i, d)
            self.connections.append(conn)

    def delete_last(self):
        if len(self.joints) > 1:
            self.joints.pop()
            self.connections.pop()

    def clear_all(self):
        while len(self.joints) > 1:
            self.joints.pop()
            self.connections.pop()

    def add_joint(self, x, y):
        joint = Joint(x, y)
        self.joints.append(joint)
        dx = self.joints[-2].x - x
        dy = self.joints[-2].y - y
        d = math.sqrt(dx * dx + dy * dy)
        conn = Connection(len(self.joints) - 2, len(self.joints) - 1, d)
        self.connections.append(conn)
        
            
    def reach(self, x, y, tol = 1):
        base = (self.joints[0].x, self.joints[0].y)
        dx = x - base[0]
        dy = y - base[1]
        dist = math.sqrt(dx * dx + dy * dy)
        body_length = sum(c.distance for c in self.connections)

        if dist > body_length:
            for i in range(len(self.joints) - 1):
                dx = self.joints[i].x - x 
                dy = self.joints[i].y - y 
                r = math.sqrt(dx * dx + dy * dy)
                di = self.connections[i].distance
                yi = di / r
                npx = (1 - yi) * self.joints[i].x + yi * x
                npy = (1 - yi) * self.joints[i].y + yi * y
                self.joints[i + 1].x = npx
                self.joints[i + 1].y = npy
        else:
            base = (self.joints[0].x, self.joints[0].y)
            dx = x - self.joints[-1].x
            dy = y - self.joints[-1].y
            dist = math.sqrt(dx * dx + dy * dy)
            while dist > tol:
                #### FORWARD REACH
                self.joints[-1].x = x
                self.joints[-1].y = y
                for i in range(len(self.joints) - 2, -1, -1):
                    dx = self.joints[i + 1].x - self.joints[i].x
                    dy = self.joints[i + 1].y - self.joints[i].y
                    r = math.sqrt(dx * dx + dy * dy)
                    di = self.connections[i].distance
                    yi = di / r
                    npx = (1 - yi) * self.joints[i+1].x + yi * self.joints[i].x
                    npy = (1 - yi) * self.joints[i+1].y + yi * self.joints[i].y
                    self.joints[i].x = npx
                    self.joints[i].y = npy

                #### BACKWARD REACH
                self.joints[0].x = base[0]
                self.joints[0].y = base[1]
                for i in range(len(self.joints) - 1):
                    dx = self.joints[i + 1].x - self.joints[i].x
                    dy = self.joints[i + 1].y - self.joints[i].y
                    r = math.sqrt(dx * dx + dy * dy)
                    di = self.connections[i].distance
                    yi = di / r
                    npx = (1 - yi) * self.joints[i].x + yi * self.joints[i + 1].x
                    npy = (1 - yi) * self.joints[i].y + yi * self.joints[i + 1].y
                    self.joints[i + 1].x = npx
                    self.joints[i + 1].y = npy

                
                dx = x - self.joints[-1].x
                dy = y - self.joints[-1].y
                dist = math.sqrt(dx * dx + dy * dy)
    
