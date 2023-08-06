from contamxpy import cxLib 
import cxResults as cxr
import cxRunSim

import os, sys
from optparse import OptionParser
import time
import threading
import multiprocessing

def checkFile(ext, fname):
    checksOut = True
    root, extension = os.path.splitext(fname) 
    if extension != ext:
        checksOut = False
    elif not os.path.exists(fname):
        checksOut = False
    return checksOut

#===================================================================================== main() =====
# Run simulations on multiple PRJ files using synchronous, multithreading, 
# and multiprocessing (fails pickling CFFi-wrapped contamx-lib).
# Provides timing of execution.
#
# Usage: test_MultiRun.py prjFile.lst -m1
#   prjFile.lst - text file contains
#   PRJs: test_GetPrjInfo.prj, test_OneFloorWpcAddMf.prj, test_OneZoneWthCtm.prj, valThreeZonesWthCtm.prj
# 
if __name__ == "__main__":
    METHOD = "Synchronous"

    # ----- Manage option parser
    parser = OptionParser(usage="%prog [options] arg1\n\targ1=list filename")
    parser.set_defaults(test_run=False)
    parser.add_option("-m", "--method", action="store", dest="run_method", type="int", default=0,
                        help="Define concurrency method: 0=Synchronous, 1=Multithread, 2=Multiprocess, 3=ProcessPool.")
    parser.add_option("-t", action="store_true", dest="test_run",
                        help="Test creation of set of files to run, but do not run the simulations.")
    parser.set_defaults(verbose=0)
    parser.add_option("-v", "--verbose", action="store", dest="verbose", type="int", default=0,
                        help="Define verbose output level: 0=Min, 1=Medium, 2=Maximum.")
    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("Need one argument:\n  arg1 = List file.")
        sys.exit(1)
    else:
        List_file_in = args[0]

    if ( not os.path.exists(List_file_in) ):
        print("ERROR: List file not found.")
        sys.exit(1)

    # Process command line options
    TEST_RUN = options.test_run
    verbose = options.verbose
    run_method = options.run_method

    strMethods = ["Synchronous", "Multi-thread", "Multi-process", "ProcessPool"]

    #----- Initialize lists -----
    #
    # Each line in List file should contain {nItemsPerLine} items.
    nItemsPerLine = 1
    prj_list = []
    cxLib_list = []

    #----- Create LOG File -----
    #
    print(f"Method = {strMethods[run_method]}")
    print(f"TEST_RUN = {str(TEST_RUN)}")
    print("Working Directory = " + os.getcwd() )
    
    #----- Read List file and populate file lists.
    # Each line contains the path of a PRJ file.
    # Comments are denoted with "#".
    nSimsToRun = 0
    nLinesRead = 0
    fd_List = open(List_file_in, "r")
    for line_in_fdList in fd_List:
        if( not line_in_fdList.rstrip('\n') ):
            continue
        # Remove white space and provide line items as list.
        itemsOnLineOfListfile = [x1.strip(' \n') for x1 in line_in_fdList.split(',')]
        if( itemsOnLineOfListfile[0][:1] == '#'):
            # Skip comment lines in List File.
            continue
        nLinesRead += 1
        if( len(itemsOnLineOfListfile) != nItemsPerLine):
            print(f"Incorrect number of parameters on line: {str(itemsOnLineOfListfile)}")
            continue
        # Verify file types have correct extensions.
        bSkipFile = False
        for file in itemsOnLineOfListfile:
            root, ext = os.path.splitext(file)
            if not checkFile(".prj", file):
                # File not found or incorrect type => skip this set of files
                bSkipFile = True
                print(f"x File not found or incorrect type: {file} {str(itemsOnLineOfListfile)}")
                continue
        if bSkipFile == True:
            continue

        # Add PRJ path to list.
        prj_list.append(itemsOnLineOfListfile[0])

        print(f"o {str(nSimsToRun+1)} Simulation to run: {str(itemsOnLineOfListfile)}")
        nSimsToRun += 1
        # End 

    print(f"Number of lines read  = {str(nLinesRead)}")
    print(f"Number of sims to run = {str(nSimsToRun)}")
    if( nSimsToRun == 0 ):
        print("*** ERROR: No simulations to run. ***")
        sys.exit(0)

    #----------------------------------------------------------------
    #------------------------------------------ Run Simulations -----
    #----------------------------------------------------------------
    if( TEST_RUN == False ):
        print(f"Run simulations on: {prj_list}.")

        time_start = time.time()

        #----- Instantiate list of contamx-lib objects
        for i in range(nSimsToRun):
            cxLib_list.append(cxLib(prj_list[i], 0, False))

        jobs = []
        results = []

        if(run_method == 0):            # No concurrency
            for myPrj in cxLib_list:
                cxRunSim.run_sim(myPrj)
        elif(run_method == 1):          # Threading
            for myPrj in cxLib_list:
                t = threading.Thread(target=cxRunSim.run_sim, args=(myPrj,))
                jobs.append(t)
        elif(run_method == 2):          # Multi-processing - Process
            # This method fails due to attempts to pickle
            #   CFFI-wrapped contamx-lib.
            for myPrj in cxLib_list:
                p = multiprocessing.Process(target=cxRunSim.run_sim, args=(myPrj,))
                jobs.append(p)
                ### TypeError: cannot pickle '_cffi_backend.__CDataOwnGC' object
        else:
            # This method seems to fail due to attempts to pickle
            #   CFFI-wrapped contamx-lib, but errors may not be displayed.
            ncpu = multiprocessing.cpu_count()
            NUM_WORKERS = ncpu - 1
            pool = multiprocessing.Pool( processes = NUM_WORKERS ) 
            print(f"NumCPUs = {ncpu}, NUM_WORKERS = {NUM_WORKERS}")
            results = [pool.apply_async(cxRunSim.run_sim, args=(myPrj,)) for myPrj in cxLib_list]
            pool.close()
            pool.join()

        if(run_method == 1 or run_method == 2):
            for j in jobs:
                j.start()
            for j in jobs:
                j.join()

    # End if(TEST_RUN)

    print(f"elapsed time = {time.time()-time_start} sec")

    sys.exit(0)

#--- End main() ---#
