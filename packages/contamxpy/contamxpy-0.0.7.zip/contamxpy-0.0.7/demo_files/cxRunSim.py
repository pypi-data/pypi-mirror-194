import contamxpy
from contamxpy import cxLib as cxl

def run_sim(cxl):
    #----- Setup Simulation for PRJ
    print(f"===== run_sim(cxLib:{cxl}, prj:{cxl.prjPath})")
    cxl.setupSimulation(1)

    #----- Get simulation run info
    dayStart = cxl.getSimStartDate()
    dayEnd   = cxl.getSimEndDate()
    secStart = cxl.getSimStartTime()
    secEnd   = cxl.getSimEndTime()
    tStep    = cxl.getSimTimeStep()

    #----- Calculate the simulation duration in seconds and total time steps
    simBegin = (dayStart - 1) * 86400 + secStart
    simEnd = (dayEnd - 1) * 86400 + secEnd
    if (simBegin < simEnd):
        simDuration = simEnd - simBegin
    else:
        simDuration = 365 * 86400 - simEnd + simBegin
    numTimeSteps = int(simDuration / tStep)

    #----- Get the current date/time after initial steady state simulation
    for i in range(numTimeSteps):
        cxl.doSimStep(1)
    cxl.endSimulation()