#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
from pyomo.environ import *
from pyomo.dae import *

Np = 24
last_solution = [False, False, False]
last_path = [(0, 0), (0, 0)]

PIPEGAPSIZE  = 100 # gap between upper and lower pipe
PIPEWIDTH = 52
BIRDWIDTH = 34
BIRDHEIGHT = 24
BIRDDIAMETER = np.sqrt(BIRDHEIGHT**2 + BIRDWIDTH**2) # the bird rotates in the game, so we use it's maximum extent
SKY = 0 # location of sky
GROUND = (512*0.79)-1 # location of ground
PLAYERX = 57 # location of bird

pipeVelx = -4
playerAccY = 1
playerFlapAcc = -14

def solve(playery, playeryVel, lowerPipes):
    x = PLAYERX
    last_xPos = []
    
    obj = 0
    
    m = ConcreteModel()
    m.flap = Var(RangeSet(0, Np-2), within=Boolean)
    m.sk = RangeSet(0, Np-1)
    m.vy = Var(m.sk)
    m.y = Var(m.sk)
    
    #print("x pos: ")
    #print(last_xPos)
    
    m.cony = ConstraintList()
    m.convy = ConstraintList()
    
    for k in range(Np):
        m.cony.add(inequality(SKY, m.y[k], GROUND))
        
    m.convy.add(m.vy[0] == playeryVel)
    m.cony.add(m.y[0] == playery)
    
    #print("add constraint successful")
    #m.cony.display()
    #m.convy.display()
    
    for k in range(Np-1):
        m.convy.add(m.vy[k+1] == m.vy[k] + playerAccY * (k//15 + 1) + playerFlapAcc * m.flap[k])
        m.cony.add(m.y[k+1] == m.y[k] + m.vy[k+1]*(k//15+1))
    
    #print("add constraint successful")
    #m.cony.display()
    #m.convy.display()

    pipeDistance = 0 # init dist from pipe center
    last_xPos += [x]
    
    for k in range(Np-1):
        dt = k // 15 + 1
        x -= dt * pipeVelx
        last_xPos += [x]
        for pipe in lowerPipes:
            distanceFromFront = pipe['x'] - x - BIRDDIAMETER
            distanceFromBack = pipe['x'] - x + PIPEWIDTH
            print("distance:")
            print("%f %f"%(distanceFromBack, distanceFromFront))
            if (distanceFromFront < 0) and (distanceFromBack > 0):
                m.convy.add(inequality((pipe['y'] - PIPEGAPSIZE), m.y[k+1], (pipe['y'] - BIRDDIAMETER)))
                pipeDistance += abs(pipe['y'] - (PIPEGAPSIZE//2) - (BIRDDIAMETER//2) - m.y[k+1]) # add distance from center
    
    obj += pipeDistance
    
    obj *= 100
    
    for k in range(Np):
        obj += abs(m.vy[k])
    
    m.obj = Objective(expr=obj, sense=minimize)
    
    try:
        print("start solve problem")
        SolverFactory('ipopt').solve(m)
        m.cony.display()
        m.convy.display()
        m.flap.display()
        m.obj.display()
        m.y.display()
        m.vy.display()
        
        print("solve successful")
        solution = m.flap[0]()
        print("solution:")
        print(solution)
        
        last_path = []
        for i in range(Np):
            last_path += [(last_xPos[i], m.y[i]())]
            
        print("last path: ")
        print(last_path)
        
        return solution, last_path
    except:
        try:
            last_solution = last_solution[1:]
            last_path = [((x-4), y) for (x, y) in last_path]
            print("solve failed")
        except:
            print("failed many times")
            return False, [(0, 0), (0, 0)]
