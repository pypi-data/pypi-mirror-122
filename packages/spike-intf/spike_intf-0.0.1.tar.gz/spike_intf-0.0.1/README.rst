Spike Wrapper Build
##########################
** REQUIRES GCC-7+ **

Spike is the RISC-V instruction set simulator used as a golden model for verifying Shakti core implementation. The wrapper for the **riscv-isa-sim** is build using the following steps. The wrapper DPI functions are called for instruction level verification.

Tested for riscv-isa-sim commitid: ``b93262af831cdfb416d19ee6fa808c5d767c9ceb``

.. code-block:: bash
    
    $ cd spike_model

    # spike build
    $ git clone https://github.com/riscv/riscv-isa-sim.git --recursive
    $ cd riscv-isa-sim
    $ git checkout b93262af831cdfb416d19ee6fa808c5d767c9ceb
    $ git apply ../spike.patch
    $ mkdir build
    $ cd build
    $ export RISCV=$PWD
    $ ../configure --prefix=$RISCV
    $ make
    $ cd ..

    # spike python wrapper build
    $ cmake .
    $ make

    # usage testing
    $ python test_spike_wrapper.py rv64imafdc test_example.elf


The model files needed for CoCoTb Verification gets generated

Spike wrapper memory map
############################

Spike wrapper code generates the shared library file for spike with the following APIs 

+---------------------------------------------------------------------------+--------------------------------------------------+
| Spike DPI                                                                 | Description                                      |
+---------------------------------------------------------------------------+--------------------------------------------------+
| void* spike_intf(char* elf_file, char* isa)                               | Create model instance with isa and load elf_file |
+---------------------------------------------------------------------------+--------------------------------------------------+
| unsigned int single_step(c_spike_intf instance)                           | Perform a single step                            |
+---------------------------------------------------------------------------+--------------------------------------------------+
| uint64_t get_variable(uint32_t address)                                   | Get value from the memory mapped address         |
+---------------------------------------------------------------------------+--------------------------------------------------+
| void set_variable(c_spike_intf instance, uint32_t address, uint64_t val)  | Set value of memory mapped address               |
+---------------------------------------------------------------------------+--------------------------------------------------+
| void destroy_sim(c_spike_intf instance)                                   | Destroy spike model instance                     |
+---------------------------------------------------------------------------+--------------------------------------------------+


The address to be specified is defined by SLSV as a state id. A brief snapshot of the same is below:

+----------+--------+
| State ID | Offset |
+----------+--------+
| PC       | 'h1020 |
+----------+--------+
| XPR      | 'h1000 |
+----------+--------+
| FPR      | 'h1021 |
+----------+--------+
| PRV      | 'h1041 |
+----------+--------+
| SSTATUS  | 'h100  |
+----------+--------+
| SIE      | 'h104  |
+----------+--------+
| STVEC    | 'h105  |
+----------+--------+
| MSTATUS  | 'h300  |
+----------+--------+
| MISA     | 'h301  |
+----------+--------+
| MIE      | 'h304  |
+----------+--------+
| MTVEC    | 'h305  |
+----------+--------+

The CSR registers follow the offset address specified in the spike model (*encoding.h*)



