# Install NGSPICE

NGSPICE was installed from source with OSDI support to use the compiled model.

**Installation Path:** `/home/ankdesh/explore/vsd-7nm/setup/ngspice_installed`

## Steps Taken

1. **Clone**
   ```bash
   git clone https://git.code.sf.net/p/ngspice/ngspice ngspice_git
   ```

2. **Configure**
   ```bash
   mkdir -p release && cd release
   ../configure --with-x --enable-xspice --disable-debug --enable-cider --with-readline=yes --enable-openmp --enable-osdi --prefix=/home/ankdesh/explore/vsd-7nm/setup/ngspice_installed
   ```

3. **Build & Install**
   ```bash
   make -j4 && make install
   ```

## Verification

The installation was verified by running the installed binary.

**Command:**
```bash
/home/ankdesh/explore/vsd-7nm/setup/ngspice_installed/bin/ngspice --version
```

**Result:** `NGSPICE 45+` is installed successfully.