# BSIM-CMG Model Setup Guide

This guide describes how to compile the BSIM-CMG Verilog-A model using the OpenVAF compiler to generate an OSDI shared library for NGSPICE.

## Prerequisites

1. **Download OpenVAF**: [fides.fe.uni-lj.si/openvaf/download/](https://fides.fe.uni-lj.si/openvaf/download/)
2. **Download BSIM-CMG Model**: [bsim.berkeley.edu/models/bsimcmg/](https://www.bsim.berkeley.edu/models/bsimcmg/)

## Compilation Walkthrough

### 1. Compilation
Use the `openvaf` binary to compile the Verilog-A source into an OSDI file.

**Command:**
```bash
./openvaf-r bsim_cmg/code/bsimcmg.va -I bsim_cmg/code -o bsimcmg.osdi
```

**Expected Output:**
```text
Finished building bsimcmg.va
```

### 2. Verification
Verify that the `bsimcmg.osdi` shared library was created in your directory.

**Command:**
```bash
ls -l bsimcmg.osdi
```

## Conclusion
The BSIM-CMG model has been successfully compiled to `bsimcmg.osdi`. This file can now be loaded into NGSPICE or other OSDI-compatible simulators.
