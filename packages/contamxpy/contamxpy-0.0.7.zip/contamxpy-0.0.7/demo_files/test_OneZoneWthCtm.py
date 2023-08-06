from contamxpy import cxLib 
import cxResults as cxr
import os, sys
from optparse import OptionParser
import typing
import numpy as np

## TEST CASES - use global variables
g_times  = np.zeros(shape=1, dtype=int)     # sec
g_Tambt  = np.zeros(shape=1, dtype=float)   # K
g_Pambt  = np.zeros(shape=1, dtype=float)   # Pa
g_WSambt = np.zeros(shape=1, dtype=float)   # m/s
g_WDambt = np.zeros(shape=1, dtype=float)   # deg
g_MFambt = np.zeros(shape=1, dtype=float)   # kg/kg
g_Tzone  = np.zeros(shape=1, dtype=float)   # K
g_PctOa  = np.zeros(shape=1, dtype=float)   # 0.0 - 1.0
g_AhsFlow= np.zeros(shape=1, dtype=float)   # m3/h-m2
g_CtrlIn = np.zeros(shape=(1,2), dtype=float) # assumes only two sets of control data

def setWthCtmData( prjName ):
    dataSetNum = 1
    #                               0    6:00:00 14:00:00 15:00:00 23:00:00 24:00:00
    times_data  = np.array([        0,     21600,   50400,   57600,   82800,   86400])
    Tambt_data  = np.array([   273.15,    293.15,  293.15,  293.15,  293.15,  293.15])
    Pambt_data  = np.array([   101325,    101325,  101325,  101325,  101325,  101325])
    WSambt_data = np.array([      0.0,     7.397,     0.0,   7.397,     0.0,     0.0])
    WDambt_data = np.array([      0.0,     270.0,     0.0,    90.0,     0.0,     0.0])
    MFambt_data = np.array([0.0023254, 0.0023254,     0.0,     0.0,     0.0,     0.0])
    Tzone_data  = np.array([   283.15,    288.15,  293.15,  298.15,  290.15,  283.15])
    #                     C        10         15       20       25       17       10
    PctOa_data  = np.array([     0.25,      0.75,     0.0,     1.0,     1.0,     1.0])
    AhsFlow_data= np.array([     10.0,       5.0,     7.5,    10.0,     9.0,     8.0])
    CtrlIn_data = np.array([ 
                           [   263.15,    268.15,  273.15,  278.15,  270.15,  263.15], # K for Tzone
                           [      100,       200,     300,     150,     0.0,  100   ]  # Multiplier on Flow
                        ])

    dataSetNum = 1
    if prjName == "test_OneZoneWthCtmStack-UseApi":
        dataSetNum = 2
        #                             0      6:00:00 12:00:00 13:00:00 24:00:00
        times_data  = np.array([      0,       21600,   43200,   46800,   86400])
        Tambt_data  = np.array([ 273.15,      273.15,  293.15,  263.15,  263.15])
        Pambt_data  = np.array([101325,       101325,  101325,  101325,  101325])
        WSambt_data = np.array([   0.0,          0.0,     0.0,     0.0,     0.0])
        WDambt_data = np.array([   0.0,          0.0,     0.0,     0.0,     0.0])
        MFambt_data = np.array([0.0023254, 0.0023254,     0.0,     0.0,     0.0])
        Tzone_data  = np.array([ 293.15,      293.15,  293.15,  303.15,  303.15])
                          #   C      20           20       20       30       30
        PctOa_data  = np.array([  0.25,        0.75,     0.0,      1.0,     1.0])
        AhsFlow_data= np.array([  10.0,         5.0,     7.5,     10.0,     8.0])
        CtrlIn_data = np.array([
                      [ 293.15,      293.15,  293.15,  303.15,  303.15],
                      [    0.0,         0.0,     0.0,     0.0,     0.0]
                    ])

    elif prjName == "valThreeZonesWthCtm-UseApi":
        dataSetNum = 3
        times_data  = np.array([        0,     86400])
        Tambt_data  = np.array([   293.15,    293.15])
        Pambt_data  = np.array([   101325,    101325])
        WSambt_data = np.array([     5.23,      5.23])
        WDambt_data = np.array([      270,       270])
        MFambt_data = np.array([0.0023254, 0.0023254])
        Tzone_data  = np.array([   293.15,    293.15])
        PctOa_data  = np.array([      1.0,       1.0])
        AhsFlow_data= np.array([      9.0,       9.0])
        CtrlIn_data = np.array([
                                [   293.15,    293.15],
                                [     0.0,       0.0 ]
                            ])

    n = len(times_data)
    t  = np.zeros(shape=n)
    Ta = np.zeros(shape=n)
    Pa = np.zeros(shape=n)
    WS = np.zeros(shape=n)
    WD = np.zeros(shape=n)
    MF = np.zeros(shape=n)
    Tz = np.zeros(shape=n)
    OA = np.zeros(shape=n)
    AF = np.zeros(shape=n)
    CI = np.zeros(shape=(2,n))

    for i in range(n):
        t[i]  =  times_data[i]
        Ta[i] = Tambt_data[i]
        Pa[i] = Pambt_data[i]
        WS[i] = WSambt_data[i]
        WD[i] = WDambt_data[i]
        MF[i] = MFambt_data[i]
        Tz[i] = Tzone_data[i]
        OA[i] = PctOa_data[i]
        AF[i] = AhsFlow_data[i]
    for ir in range(2):
        for ic in range(n):
            CI[ir,ic] = CtrlIn_data[ir,ic]

    print(f"\nUSING DATA SET {prjName} NUMBER {dataSetNum} !!!\n")
    print(f"time:\t{t}\nTambt:\t{Ta}\nPambt:\t{Pa}\nWSpeed:\t{WS}\nWDir:\t{WD}\nMFambt:\t{MF}\nTzone:\t{Tz}\nPctOA:\t{OA}\nFAhs:\t{AF}\nCtrlIn:\t{CI}\n")
    '''
    for i in range(2):
        for j in range(n):
            print(f"{i},{j}={CI[i][j]}\t")
        print("\n")
    '''
    return t, Ta, Pa, WS, WD, MF, Tz, OA, AF, CI

#============================================================================ setWthCtmInit() =====
# Set the initial conditions for the SetAmbt API test.
# This function is set as a parameter to instantiation of cxLib
#   to be called by the contamxpy.prjDataReadyFcnP() in order to set 
#   ambient boundary conditions for steady-state initialization.
# NOTE: The parameter {cxl as cxLib} is passed through contamx-lib to 
#   contamxpy.prjDataReadyFcnP() which in turn passes it to this function
#   to distinguish the instance of cxLib to be used.
#
def setWthCtmInit( cxl ):
    global g_times, g_Tambt, g_Pambt, g_WSambt, g_WDambt, g_MFambt, g_Tzone, g_PctOa, g_AhsFlow, g_CtrlIn
    ### DEBUG
    print(f"setWthCtmInit({cxl})")
    cxl.setAmbtPressure(g_Pambt[0])
    cxl.setAmbtWindSpeed(g_WSambt[0])
    cxl.setAmbtWindDirection(g_WDambt[0])
    cxl.setAmbtMassFraction(0, g_MFambt[0])
    cxl.setAmbtTemperature(g_Tambt[0])
    # Vary Tzone by iz index to show clear differences when plotted.
    for iz in range(cxl.nZones):
        cxl.setZoneTemperature(iz+1, g_Tzone[0]+iz)
    for ij in range(cxl.nDuctJunctions):
        cxl.setJunctionTemperature(ij+1, g_Tzone[0]+ij)
    fOA = g_PctOa[0]
    for ia in range(cxl.nAhs):
        cxl.setAhsPercentOa(ia+1, fOA)
        fOA *= 0.95
    fFlow = g_AhsFlow[0]
    for ih in range(cxl.nAhs):
        setAhsFlows(cxl, ih, fFlow)
        #fFlow *= 0.95
    for ic in range(cxl.nInputControls):
        j = ic % 2
        cxl.setInputControlValue(ic+1, g_CtrlIn[j][0])

#================================================================================ setWthCtm() =====
# Update conditions when appropriate.
def setWthCtm( cxl, date, time, step, index ) -> int:
    # Check if it's time to change to the next set of Ambient data.
    global g_times, g_Tambt, g_Pambt, g_WSambt, g_WDambt, g_MFambt, g_Tzone, g_PctOa, g_AhsFlow, g_CtrlIn
    if index >= len(g_times):
        return index
    if (time == g_times[index]):
        ###print(f"setWthCtm({date} {time})")
        cxl.setAmbtTemperature(g_Tambt[index])
        cxl.setAmbtPressure(g_Pambt[index])
        cxl.setAmbtWindSpeed(g_WSambt[index])
        cxl.setAmbtWindDirection(g_WDambt[index])
        cxl.setAmbtMassFraction(0, g_MFambt[index])
        # Vary Tzone by iz index to show clear differences when plotted.
        for iz in range(cxl.nZones):
            cxl.setZoneTemperature(iz+1, g_Tzone[index]+iz)
        for ij in range(cxl.nDuctJunctions):
            cxl.setJunctionTemperature(ij+1, g_Tzone[index]+ij)
        fOA = g_PctOa[index]
        for ia in range(cxl.nAhs):
            cxl.setAhsPercentOa(ia+1, fOA)
            fOA *= 0.95
        fFlow = g_AhsFlow[index]
        for ih in range(cxl.nAhs):
            setAhsFlows(cxl, ih, fFlow)
            #fFlow *= 0.95
        for ic in range(cxl.nInputControls):
            j = ic % 2
            cxl.setInputControlValue(ic+1, g_CtrlIn[j][index])
        index = index + 1 
    return index

#============================================================================== setAhsFlows() =====
def setAhsFlows(cxl : cxLib, ahsIndex, val):
    ahs = cxl.AHSs[ahsIndex]
    ### print(f"setAhsFlows({ahs.name})")
    # Set flow per zone floor area m3/h-m2
    Hf = 3.0 # assume h=3
    pathTypeStr = "SUPPLY"
    for path in ahs.supply_points:
        Zone  = cxl.zones[path.to_zone-1]
        Vzone = Zone.Vol                # m3
        Azone = Vzone / Hf              # m2
        Vdot  = val * Azone             # m3/h-m2 * m2 = m3/h
        Mdot  = Vdot * 1.2041 / 3600.0  # kg/s
        ### print(f"\t{pathTypeStr}\tp{path.nr}/z{path.to_zone}:\t{val:.2f} m3/h-m2\t{Vzone:.2f} m3\t({Azone} m2)\t{Vdot:.2f} m3/h\t{Mdot:.5f} kg/s ")
        cxl.setAhsSupplyReturnFlow(path.nr, Mdot)
    pathTypeStr = "RETURN"
    for path in ahs.return_points:
        Zone = cxl.zones[path.from_zone-1]
        Vzone = Zone.Vol                # m3
        Azone = Vzone / Hf              # m2
        Vdot  = val * Azone             # m3/h-m2 * m2 = m3/h
        Mdot  = Vdot * 1.2041 / 3600.0  # kg/s
        ### print(f"\t{pathTypeStr}\tp{path.nr}/z{path.from_zone}:\t{val:.2f} m3/h-m2\t{Vzone:.2f} m3\t({Azone} m2)\t{Vdot:.2f} m3/h\t{Mdot:.5f} kg/s ")
        cxl.setAhsSupplyReturnFlow(path.nr, Mdot)

#===================================================================================== main() =====
def main():
    global g_times, g_Tambt, g_Pambt, g_WSambt, g_WDambt, g_MFambt, g_Tzone, g_PctOa, g_AhsFlow, g_CtrlIn

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
        # Get PRJ file name
        prjPath  = args[0]

    if ( not os.path.exists(prjPath) ):
        print("ERROR: PRJ file not found.")
        return

    root, ext = os.path.splitext(prjPath)
    prjName = os.path.basename(root)

    msg_cmd = "Running test_OneZoneWthCtm.py: arg1 = " + args[0] + " " + str(options)
    print(msg_cmd, "\n")

    #----- Initialize Data Set for Boundary Conditions and Controls.
    #     
    print(f"\n=====\nDataSetName = {prjName}\n=====\n")
    g_times, g_Tambt, g_Pambt, g_WSambt, g_WDambt, g_MFambt, g_Tzone, g_PctOa, g_AhsFlow, g_CtrlIn = setWthCtmData(prjName)

    if verbose > 1:
        print(f"cxLib attributes =>\n{chr(10).join(map(str, dir(cxLib)))}\n")

    #----- Initialize contamx-lib object w/ wpMode and cbOption.
    #      wpMode = 0 => use wind pressure profiles, WTH and CTM files or associated API calls.
    #      cbOption = True => set callback function to get PRJ INFO from the ContamXState.
    myPrj = cxLib(prjPath, 0, True, setWthCtmInit)
    
    myPrj.setVerbosity(verbose)
    if verbose > 1:
        print(f"BEFORE setupSimulation()\n\tnCtms={myPrj.nContaminants}\n\tnZones={myPrj.nZones}\n\tnPaths={myPrj.nPaths}\n" )
    
    #----- Query State for Version info
    verStr = myPrj.getVersion()
    if verbose >= 0:
        print(f"getVersion() returned {verStr}.")

    #----------------------------------------------------------------
    #------------------------------------ Initialize Simulation -----
    #----------------------------------------------------------------
    myPrj.setupSimulation(1)

    #----- Initialize result files
    fResMfList = []
    fResEnvExfilList = []
    root, ext = os.path.splitext(prjPath)
    fNameResMf = root + "_Mf"
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

    #----- Get simulation run info
    dayStart = myPrj.getSimStartDate()
    dayEnd   = myPrj.getSimEndDate()
    secStart = myPrj.getSimStartTime()
    secEnd   = myPrj.getSimEndTime()
    tStep    = myPrj.getSimTimeStep()
 
    #----- Calculate the simulation duration in seconds and total time steps
    simBegin = (dayStart - 1) * 86400 + secStart
    simEnd = (dayEnd - 1) * 86400 + secEnd
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
    wthIndex = 1

    for i in range(numTimeSteps):
        #------------------------------------------------------------
        #----- Tasks to perform BEFORE current time step.
        #------------------------------------------------------------
        wthIndex = setWthCtm( myPrj, currentDate, currentTime, tStep, wthIndex)

        #------------------------------------------------------------
        # Run next time step.
        #------------------------------------------------------------
        myPrj.doSimStep(1)

        #------------------------------------------------------------
        #----- Tasks to perform AFTER current time step.
        #------------------------------------------------------------
        currentDate = myPrj.getCurrentDayOfYear()
        currentTime = myPrj.getCurrentTimeInSec()

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

    #----------------------------------------------------------------
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
