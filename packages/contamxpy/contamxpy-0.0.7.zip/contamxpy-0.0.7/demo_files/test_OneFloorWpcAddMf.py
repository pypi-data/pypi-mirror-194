from contamxpy import cxLib 
import cxResults as cxr
import os, sys
from optparse import OptionParser

## TEST CASE - testOneZoneWpc-UseApi.prj

#======================================================================================= DATA =====
#             00:00,     01:00,     01:05,     06:00,     06:05,     12:00,     12:05,     13:00,     18:00,     18:05,     24:00
# time in seconds.
times = [         0,      3600,      3900,     21600,     21900,     43200,     43500,     46800,     64800,     65100,     86400 ]
# p1wp[] wind pressure units, Pa.  
p1wp  = [  2.508542,  2.508542,  2.508542,  2.508542,  2.508542,  2.508542, -2.508542, -2.508542, -2.508542, -2.508542, -2.508542 ]
# p2wp[] wind pressure units, Pa.  
p2wp  = [ -2.508542, -2.508542, -2.508542, -2.508542, -2.508542, -2.508542,  2.508542,  2.508542,  2.508542,  2.508542,  2.508542 ]
# p1mf0[] mass fraction units, kg_contaminant/kg_air.  
p1mf0 = [         0,      0.01,      0.01,      0.00,         0,         0,         0,         0,         0,         0,         0 ]
# p2mf0[] mass fraction units, kg_contaminant/kg_air.  
p2mf0 = [         0,         0,         0,         0,         0,         0,         0,         0,         0,         0,         0 ]
# p1mf1[] mass fraction units, kg_contaminant/kg_air.  
p1mf1 = [         0,         0,         0,         0,         0,         0,         0,         0,         0,         0,         0 ]
# p2mf1[] mass fraction units, kg_contaminant/kg_air.  
p2mf1 = [         0,         0,         0,         0,         0,         0,         0,      0.02,      0.00,         0,         0 ]

#============================================================================== Set Ambt Data =====
# It is taken for granted that various properties of the PRJ are known:
# - the envIndex of the two flow paths
# - the number of contaminants in the PRJ
#
def setEnvelopePathsWPCInit( cxl ):
    ### print(f"setEnvelopePathsWPCInit({t_index})")
    cxl.setEnvelopeWP(1, p1wp[0])     # envIndex 1
    cxl.setEnvelopeWP(2, p2wp[0])     # envIndex 2
    cxl.setEnvelopeMF(1, 0, p1mf0[0]) # envIndex 1, contaminant 0
    cxl.setEnvelopeMF(2, 0, p2mf0[0]) # envIndex 2, contaminant 0
    cxl.setEnvelopeMF(1, 1, p1mf1[0]) # envIndex 1, contaminant 1
    cxl.setEnvelopeMF(2, 1, p2mf1[0]) # envIndex 2, contaminant 1
 
# Update conditions when appropriate.
def setEnvelopePathsWPC( cxl, time, date, step, t_index ) -> int:
    # Check if it's time to change to the next set of Ambient data.
    ### print(f"setEnvelopePathsWPC({time},{date},{step},{t_index})")
    if t_index >= len(times):
        return t_index
    if (time == times[t_index]):
        ### print(f"Setting Envelope data...")
        cxl.setEnvelopeWP(1, p1wp[t_index])
        cxl.setEnvelopeWP(2, p2wp[t_index])
        cxl.setEnvelopeMF(1, 0, p1mf0[t_index])
        cxl.setEnvelopeMF(2, 0, p2mf0[t_index])
        cxl.setEnvelopeMF(1, 1, p1mf1[t_index])
        cxl.setEnvelopeMF(2, 1, p2mf1[t_index])
        t_index = t_index + 1
    return t_index

#===================================================================================== main() =====
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
    #      wpMode = 1 => use WPC-like API calls.
    #      cbOption = True => set callback function to get PRJ INFO from the ContamXState.
    myPrj = cxLib(prjPath, 1, True, setEnvelopePathsWPCInit)
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
    fResEnvExfilList = []
    root, ext = os.path.splitext(prjPath)
    fNameResFlow = root + "_Flow.txt"
    fNameResTotalExfil = root + "_Exfil.txt"
    fNameResControl = root + "_Control.txt"
    fResFlow = open(fNameResFlow, "w")
    fResExfil = open(fNameResTotalExfil, "w")
    for ic in range(myPrj.nContaminants):
        fName = root + "_Mf_" + myPrj.contaminants[ic] + ".txt"
        file = open(fName, "w")
        fResMfList.append(file)
        fName = root + "_Exfil_" + myPrj.contaminants[ic] + ".txt"
        file = open(fName, "w")
        fResEnvExfilList.append(file)
    totalEnvExfil = [0.0] * myPrj.nContaminants
    if( myPrj.nOutputControls > 0 ):
        fResControl = open(fNameResControl,"w")

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
    # Write headers
    for ic in range(myPrj.nContaminants):
        cxr.writeMfZones(fResMfList[ic], True, myPrj, currentDate, currentTime, ic)
        cxr.writeEnvExfil(fResEnvExfilList[ic], True, myPrj, -1, -1, -1)
    cxr.writeAirflowRates(fResFlow, True, myPrj, -1, -1)
    if( myPrj.nOutputControls > 0 ):
        cxr.writeControls(fResControl, True, myPrj, -1, -1)
    
    # Write initial values
    for ic in range(myPrj.nContaminants):
        cxr.writeMfZones(fResMfList[ic], False, myPrj, currentDate, currentTime, ic)
    cxr.writeAirflowRates(fResFlow, False, myPrj, currentDate, currentTime)
    if( myPrj.nOutputControls > 0 ):
        cxr.writeControls(fResControl, False, myPrj, currentDate, currentTime)

    #----------------------------------------------------------------
    #--------------------------------- Run Transient Simulation -----
    #----------------------------------------------------------------
    wpcIndex = 1

    for i in range(numTimeSteps):
        #------------------------------------------------------------
        #----- Tasks to perform BEFORE current time step.
        #------------------------------------------------------------
        wpcIndex = setEnvelopePathsWPC( myPrj, currentTime, currentDate, tStep, wpcIndex)

        #------------------------------------------------------------
        # Run next time step.
        #------------------------------------------------------------
        myPrj.doSimStep(1)

        #------------------------------------------------------------
        #----- Tasks to perform AFTER current time step.
        #------------------------------------------------------------
        currentDate = myPrj.getCurrentDayOfYear()
        currentTime = myPrj.getCurrentTimeInSec()

        #----- Add mass to zone.
        # NOTE: This will show up in the result output of both CONTAM and this driver.
        if( currentTime == (2*3600)):
            myPrj.setZoneAddMass(1, 2, 1.0)
        elif( currentTime == (15*3600)):
            myPrj.setZoneAddMass(2, 2, 2.0)

        #----- Output results of time step just performed.
        for ic in range(myPrj.nContaminants):
            cxr.writeMfZones(fResMfList[ic], False, myPrj, currentDate, currentTime, ic)
        cxr.calcEnvExfil(myPrj, totalEnvExfil)
        for ic in range(myPrj.nContaminants):
            cxr.writeEnvExfil(fResEnvExfilList[ic], False, myPrj, currentDate, currentTime, ic)
        cxr.writeAirflowRates(fResFlow, False, myPrj, currentDate, currentTime)
        if( myPrj.nOutputControls > 0 ):
            cxr.writeControls(fResControl, False, myPrj, currentDate, currentTime)

        #----- End of simulation loop

    #----- Output total envelope exfiltration.
    #      Should be the same as CSM file.
    print(f"totalEnvExfil[] final:\n\t{myPrj.contaminants}\n\t{totalEnvExfil}")
    for i in range(myPrj.nContaminants):
        fResExfil.write(f"{myPrj.contaminants[i]}\t")
    fResExfil.write("\n")
    for i in range(myPrj.nContaminants):
        fResExfil.write(f"{totalEnvExfil[i]}\t")
    fResExfil.write("\tkg\n")

    myPrj.endSimulation()

    for ic in range(myPrj.nContaminants):
        fResMfList[ic].close
        fResEnvExfilList[ic].close
    fResFlow.close()
    fResExfil.close()
    if( myPrj.nOutputControls > 0 ):
        fResControl.close()

# --- End main() ---#

if __name__ == "__main__":
    main()
