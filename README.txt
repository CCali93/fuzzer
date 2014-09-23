======================================================================================================
|                                                SETUP                                                |
======================================================================================================

1. Install request and lxml libraries for python
2. Run the program on command line:
    python fuzz.py [discover | test] url OPTIONS



=======================================================================================================
|                                                COMMANDS                                              |
=======================================================================================================

discover    Output a comprehensive, human-readable list of all discovered inputs to the system.
            Techniques include both crawling and guessing.

***************************************** NOT YET IMPLEMENTED ******************************************

test        Discover all inputs, then attempt a list of exploit vectors on those inputs.
            Report potential vulnerabilities.



========================================================================================================
|                                                OPTIONS                                                |
========================================================================================================

--custom-auth=string     Signal that the fuzzer should use hard-coded authentication for an application.
    --custom-auth=dvwa
    --custom-auth=bodgeit

Discover options:
    --common-words=file    Newline-delimited file of common words to be used in page guessing and input
                           guessing.

****************************************** NOT YET IMPLEMENTED ******************************************

Test options:
    --vectors=file         Newline-delimited file of common exploits to vulnerabilities.
    --sensitive=file       Newline-delimited file data that should never be leaked.
                           It's assumed that this data is in the application's database (e.g. test data),
                           but is not reported in any response.
    --random=[true|false]  When off, try each input to each page systematically.  When on, choose a random
                           page, then a random input field and test all vectors. Default: false.
    --slow=500             Number of milliseconds considered when a response is considered "slow".
                           Default is 500 ms.