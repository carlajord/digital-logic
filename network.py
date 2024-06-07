import os, sys
import numpy as np, pandas as pd

class Elements():
    def __init__(self, label) -> None:
        self.id = None
        self.label = label
        self.upcon = []
        self.downcon = []

    def connect(self, upcon=None, downcon=None):
        if upcon: self.upcon.append(upcon)
        if downcon: self.upcon.append(downcon)

    def disconnect(self, con):
        self

class Source(Elements):
    def __init__(self, label, conn) -> None:
        super().__init__(label, conn)

        # generate unique id

    def compute(self):
        return 1
    
    

class Sink(Elements):

    def compute(con_signal):
        return con_signal

class Gate(Elements):
    # valves
    def __init__(self, status) -> None:
        self.status = status

class Node(Elements):
    def __init__(self) -> None:
        pass

class Observer(Elements):
    # equipment or instrument
    def __init__(self) -> None:
        pass

class Connector(Elements):
    # lines
    def __init__(self) -> None:
        pass

