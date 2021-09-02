

 NAS Parallel Benchmarks 3.4 -- BT Benchmark

 No input file inputbt.data. Using compiled defaults
 Size:  102x 102x 102  (class B)
 Iterations:  200    dt:   0.0003000
 Total number of processes:     16

 Time step    1
 Time step   20
 Time step   40
 Time step   60
 Time step   80
 Time step  100
 Time step  120
 Time step  140
 Time step  160
 Time step  180
 Time step  200
 Verification being performed for class B
 accuracy setting for epsilon =  0.1000000000000E-07
 Comparison of RMS-norms of residual
           1 0.1423359722929E+04 0.1423359722929E+04 0.1086261588063E-13
           2 0.9933052259015E+02 0.9933052259015E+02 0.2145995160094E-14
           3 0.3564602564454E+03 0.3564602564454E+03 0.9727447836926E-14
           4 0.3248544795908E+03 0.3248544795908E+03 0.8574077622964E-14
           5 0.3270754125466E+04 0.3270754125466E+04 0.7507857822963E-14
 Comparison of RMS-norms of solution error
           1 0.5296984714094E+02 0.5296984714094E+02 0.4694934400213E-14
           2 0.4463289611567E+01 0.4463289611567E+01 0.1253677115106E-13
           3 0.1312257334221E+02 0.1312257334221E+02 0.7580524064319E-14
           4 0.1200692532356E+02 0.1200692532356E+02 0.9616383166343E-14
           5 0.1245957615104E+03 0.1245957615104E+03 0.1243206947957E-13
 Verification Successful


 BT Benchmark Completed.
 Class           =                        B
 Size            =            102x 102x 102
 Iterations      =                      200
 Time in seconds =                   169.10
 Total processes =                       16
 Active processes=                       16
 Mop/s total     =                  4152.40
 Mop/s/process   =                   259.53
 Operation type  =           floating point
 Verification    =               SUCCESSFUL
 Version         =                    3.4.2
 Compile date    =              30 Jun 2021

 Compile options:
    MPIFC        = mpif90
    FLINK        = $(MPIFC)
    FMPI_LIB     = (none)
    FMPI_INC     = (none)
    FFLAGS       = -O3
    FLINKFLAGS   = $(FFLAGS)
    RAND         = (none)


 Please send feedbacks and/or the results of this run to:

 NPB Development Team 
 Internet: npb@nas.nasa.gov

