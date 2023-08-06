#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : generate.py
# License           : MIT license <Check LICENSE>
# Author            : Anderson Ignacio da Silva (aignacio) <anderson@aignacio.com>
# Date              : 20.02.2023
# Last Modified Date: 26.02.2023
import logging
import os
import sys
import shutil
from ipsocgen.common.constants import options,base_module
from ipsocgen.common.modules import *
from tabulate import tabulate
from jinja2 import Environment, FileSystemLoader

def soc_gen(soc, soc_name, desc, output):
    mst = soc['masters']
    slv = soc['slaves']

    soc_cfg = {}
    soc_cfg['clk'] = soc['clk']['clk_int']
    soc_cfg['rst'] = soc['rst']['rst_int']
    soc_cfg['txn_id'] = soc['txn_id_width']

    pll = {}
    dma_info = {}
    hdl_obj = []

    # Clocks and resets first
    hdl_obj.append(Clock(soc))
    hdl_obj.append(Reset(soc))

    # Crossbar
    bus = Axi4Bus(soc)
    hdl_obj.append(bus)

    # Masters
    for master in _soc_master(bus, soc, soc_cfg, dma_info):
        hdl_obj.append(master)

    # Slaves
    for slave in _soc_slaves(bus, soc, soc_cfg, dma_info):
        hdl_obj.append(slave)

    # RTL object generation
    global_rtl = ''

    # Module Header
    global_rtl += ModuleHeader(soc, soc_name, desc, _soc_io(hdl_obj)).get_hdl()

    # Signals to be first declared
    for obj in hdl_obj:
        for ip in obj.get_signals():
            global_rtl += ip
            global_rtl += '\n'
    global_rtl += '\n'

    for obj in hdl_obj:
        global_rtl += obj.get_hdl()

    global_rtl += '\nendmodule'

    _gen_design_files(soc_name, global_rtl, hdl_obj, output)

def _gen_design_files(soc_name, global_rtl, hdl_obj, out_dir):
    types = []
    for obj in hdl_obj:
        acc_type = obj.get_acc_type()
        if (acc_type not in types) and (acc_type != None):
            types.append(obj.get_acc_type())

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    else:
        logging.warning('Overwriting previous '+str(out_dir)+' directory')
        shutil.rmtree(out_dir)
        os.mkdir(out_dir)

    rtl_out = os.path.join(out_dir, soc_name+".sv")
    soc_rtl = open(rtl_out, "w")
    soc_rtl.write(global_rtl)
    soc_rtl.close()

def _soc_slaves(bus, soc, soc_cfg, dma_info):
    hdl_obj = []
    mmap = bus.get_mmap()
    for slave, slave_desc in soc['slaves'].items():
        if slave_desc['type'] == 'ram_mem':
            iram = Axi4MemRAM(slave_desc, soc_cfg, slave)
            hdl_obj.append(iram)
        elif slave_desc['type'] == 'rom_mem':
            irom = Axi4MemROM(slave_desc, soc_cfg, slave)
            hdl_obj.append(irom)
        elif slave_desc['type'] == 'acc_dma':
            master = dma_info[slave_desc['name']]
            dma = Axi4DMA(slave_desc, soc_cfg, slave, master)
            hdl_obj.append(dma)
        elif slave_desc['type'] == 'acc_uart':
            uart = Axi4UART(slave_desc, soc_cfg, slave)
            hdl_obj.append(uart)
        elif slave_desc['type'] == 'acc_irq':
            irq_ctrl = Axi4Irq(slave_desc, soc_cfg, slave, mmap)
            hdl_obj.append(irq_ctrl)
        elif slave_desc['type'] == 'acc_timer':
            timer = Axi4Timer(slave_desc, soc_cfg, slave, mmap)
            hdl_obj.append(timer)
        elif slave_desc['type'] == 'acc_custom_slave':
            custom = Axi4AccCustomSlave(slave_desc, soc_cfg, slave, mmap)
            hdl_obj.append(custom)
        elif slave_desc['type'] == 'acc_rst':
            rst = Axi4RstCtrl(slave_desc, soc_cfg, slave, mmap)
            hdl_obj.append(rst)
        else:
            logging.warning('Unknown slave - '+slave_desc['type'])
    return hdl_obj

def _soc_master(bus, soc, soc_cfg, dma_info):
    hdl_obj = []
    cpu_included = 0
    for master, master_desc in soc['masters'].items():
        if master_desc['type'] == 'cpu_nox':
            if cpu_included == 0:
                cpu_included = 1
                hdl_obj.append(NoXCpuRV(soc, bus.get_mmap()))
        elif master_desc['type'] == 'acc_dma':
            dma_info[master_desc['name']] = master
            logging.debug('Master '+master_desc['type']+
                          ' will be added later in the slave side')
        elif master_desc['type'] == 'acc_custom_master':
            custom = Axi4AccCustomMaster(master_desc, soc_cfg, master)
            hdl_obj.append(custom)
        else:
            logging.warning('Unknown master type! - '+master_desc['type'])
    if cpu_included == 0:
        logging.error('CPU not included in masters!')
        sys.exit(1)
    return hdl_obj

def _soc_io(hdl_obj):
    io_list = []
    input_signals = []
    output_signals = []
    for obj in hdl_obj:
        input_s = obj.get_io()['in']
        output_s = obj.get_io()['out']
        for i in input_s:
            if i not in input_signals:
                input_signals.append(i)
        for j in output_s:
            if j not in output_signals:
                output_signals.append(j)

    for i in range(len(input_signals)):
        input_signals[i] = 'input\t\t'+input_signals[i]
        io_list.append(input_signals[i])
    for i in range(len(output_signals)):
        output_signals[i] = 'output\t'+output_signals[i]
        io_list.append(output_signals[i])

    return io_list
