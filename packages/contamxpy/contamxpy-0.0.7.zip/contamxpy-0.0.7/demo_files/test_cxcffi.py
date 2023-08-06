from contamxpy import cxLib 
import cxResults as cxr
import os, sys
from optparse import OptionParser

#===================================================================================== main() =====
# This program takes the full name of a PRJ file and simply runs the simulation
# from beginning to end.
def main():
    #----- Manage option parser
    parser = OptionParser(usage="%prog [options] arg1\n\targ1=PRJ filename\n")
    parser.set_defaults(verbose=0)
    parser.add_option("-v", "--verbose", action="store", dest="verbose", type="int", default=0,
                        help="define verbose output level: 0=Min, 1=Medium, 2=Maximum.")
    (options, args) = parser.parse_args()

    #----- Process command line options -v
    verbose = options.verbose

    if len(args) != 1:
        parser.error("Need one argument:\n  arg1 = PRJ file.")
        return
    else:
        prjPath  = args[0]

    if ( not os.path.exists(prjPath) ):
        print("ERROR: PRJ file not found.")
        return

    msg_cmd = "Running test_cxcffi.py: arg1 = " + args[0] + " " + str(options)
    print(msg_cmd, "\n")

    if verbose > 1:
        print(f"cxLib attributes =>\n{chr(10).join(map(str, dir(cxLib)))}\n")

    #----- Initialize contamx-lib object w/ wpMode and cbOption.
    #      wpMode = 0 => use wind pressure profiles, WTH and CTM files or associated API calls.
    #      cbOption = True => set callback function to get PRJ INFO from the ContamXState.
    myPrj = cxLib(prjPath, 0, True)
    myPrj.setVerbosity(verbose)
    if verbose > 1:
        print(f"BEFORE setupSimulation()\n\tnCtms={myPrj.nContaminants}\n\tnZones={myPrj.nZones}\n\tnPaths={myPrj.nPaths}\n" )
    
    #----- Query State for Version info
    verStr = myPrj.getVersion()
    if verbose >= 0:
        print(f"getVersion() returned {verStr}.")

    #----- Setup Simulation for PRJ
    myPrj.setupSimulation(1)

    #----- Initialize result files
    fResMfList = []
    root, ext = os.path.splitext(prjPath)
    fNameResFlow = root + "_Flow.txt"
    fResFlow = open(fNameResFlow, "w")
    for ic in range(myPrj.nContaminants):
        fName = root + "_Mf_" + myPrj.contaminants[ic] + ".txt"
        file = open(fName, "w")
        fResMfList.append(file)

    dayStart = myPrj.getSimStartDate()
    dayEnd   = myPrj.getSimEndDate()
    secStart = myPrj.getSimStartTime()
    secEnd   = myPrj.getSimEndTime()
    tStep    = myPrj.getSimTimeStep()

    simBegin = (dayStart - 1) * 86400 + secStart
    simEnd = (dayEnd - 1) * 86400 + secEnd
 
    #----- Calculate the simulation duration in seconds and total time steps
    if (simBegin < simEnd):
        simDuration = simEnd - simBegin
    else:
        simDuration = 365 * 86400 - simEnd + simBegin
    numTimeSteps = int(simDuration / tStep)
 
    #----- Get the current date/time after initial steady state simulation
    currentDate = myPrj.getCurrentDayOfYear()
    currentTime = myPrj.getCurrentTimeInSec()
    if verbose > 0:
        print(f"Sim days = {dayStart}:{dayEnd}")
        print(f"Sim times = {secStart}:{secEnd}")
        print(f"Sim time step = {tStep}")
        print(f"Number of steps = {numTimeSteps}")

    #----- Output initial results.
    ###cxr.printZoneMf(myPrj, currentDate, currentTime, myPrj.nZones, myPrj.nContaminants)\
    # Write headers
    for ic in range(myPrj.nContaminants):
        cxr.writeMfZones(fResMfList[ic], True, myPrj, currentDate, currentTime, ic)
    cxr.writeAirflowRates(fResFlow, True, myPrj, -1, -1)
    
    # Write initial values
    for ic in range(myPrj.nContaminants):
        cxr.writeMfZones(fResMfList[ic], False, myPrj, currentDate, currentTime, ic)
    cxr.writeAirflowRates(fResFlow, False, myPrj, currentDate, currentTime)

    #----- Run Simulation
    for i in range(numTimeSteps):
        # Tasks to perform BEFORE current time step.

        myPrj.doSimStep(1)

        # Tasks to perform AFTER current time step.
        currentDate = myPrj.getCurrentDayOfYear()
        currentTime = myPrj.getCurrentTimeInSec()
        if verbose > 1:
            print(f"{i}\t{currentDate},{currentTime}")

        for ic in range(myPrj.nContaminants):
            cxr.writeMfZones(fResMfList[ic], False, myPrj, currentDate, currentTime, ic)
        cxr.writeAirflowRates(fResFlow, False, myPrj, currentDate, currentTime)

    myPrj.endSimulation()

    for ic in range(myPrj.nContaminants):
        fResMfList[ic].close
    fResFlow.close()

# --- End main() ---#

if __name__ == "__main__":
    main()
