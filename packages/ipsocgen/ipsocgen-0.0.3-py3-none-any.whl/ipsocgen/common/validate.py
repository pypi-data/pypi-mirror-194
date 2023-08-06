import logging
import argparse
import pathlib
import sys
import yaml
from ipsocgen.common.constants import options, CustomFormatter
from cerberus import Validator

def validate_config(args):
    try:
        cfg = yaml.safe_load(args['config'])
    except yaml.YAMLError as exc:
        logging.error('Error while parsing YAML file:')
        if hasattr(exc, 'problem_mark'):
            if exc.context != None:
                logging.error('  parser says\n'+str(exc.problem_mark)+'\n  '+
                              str(exc.problem)+' '+str(exc.context)+
                              '\nPlease correct data and retry.')
                sys.exit(1)
            else:
                logging.error('  parser says\n'+str(exc.problem_mark)+'\n  '+
                              str(exc.problem)+
                              '\nPlease correct data and retry.')
                sys.exit(1)
        else:
            logging.error('Something went wrong while parsing yaml file')
            sys.exit(1)
    logging.debug('YAML file parse done without errors')

    sch_cfg = Validator(yaml.safe_load(open(options.sch_cfg,'r')))
    sch_cfg.allow_unknown = True
    sch_cfg.require_all = True

    # Validate all main entries
    if sch_cfg.validate(cfg) == False:
        logging.error(sch_cfg.errors)
        return False, cfg

    # Check number of masters/slaves
    if cfg['type'] == 'soc':
        if 'soc_desc' not in cfg.keys():
            logging.error('soc_desc not present in the cfg file')
            return False, cfg

        status, cfg_after = validate_soc(cfg)

        if status == False:
            return False, cfg

        logging.info('Valid YAML configuration - basic check')
        return True, cfg

def validate_soc(cfg):
    soc = cfg['soc_desc']
    there_is_a_dma = 0

    # Check if boot addr exist in case of boot.type == slave
    if soc['proc']['boot']['type'] == 'slave':
        if soc['proc']['boot']['slave'] >= soc['num_slaves']:
            logging.error('Boot Address of unknown slave')
            return False, cfg

    if soc['num_masters'] != len(soc['masters']):
        logging.error('Missing master declaration num_master is '+
                      str(soc['num_masters'])+
                      ' but only '+str(len(soc['masters']))+
                      ' were declared!')
        return False, cfg
    if soc['num_slaves'] != len(soc['slaves']):
        logging.error('Missing slave declaration num_slaves is '+
                      str(soc['num_slaves'])+
                      ' but only '+str(len(soc['slaves']))+
                      ' were declared!')
        return False, cfg
    # Master check
    sch_master = Validator(yaml.safe_load(open(options.sch_master,'r')))
    sch_master.allow_unknown = True
    sch_master.require_all = True
    unique_master_name = []
    for master, master_desc in soc['masters'].items():
        if master_desc['type'] == 'acc_dma':
            there_is_a_dma = 1
        if sch_master.validate(master_desc) == False:
            logging.error("Error on master "+str(master_desc))
            logging.error(sch_master.errors)
            return False, cfg
        else:
            if master_desc['name'] not in unique_master_name:
                unique_master_name.append(master_desc['name'])
            else:
                logging.error("Error on master "+str(master)+" not unique name!")
                return False, cfg
    logging.debug('Valid master configuration')

    # If there's a DMA, check if the number of master == slaves
    if there_is_a_dma != 0:
        if _validate_dma(soc) != 0:
            logging.error("Number of m.dma != s.dma!")
            return False, cfg

    # Slave check
    sch_slave = Validator(yaml.safe_load(open(options.sch_slave,'r')))
    sch_slave.allow_unknown = True
    sch_slave.require_all = True
    unique_slave_name = []
    acc_rst_found = 0
    for slave, slave_desc in soc['slaves'].items():
        if sch_slave.validate(slave_desc) == False:
            logging.error("Error on slave "+str(slave_desc))
            logging.error(sch_slave.errors)
            return False, cfg
        else:
            if slave_desc['name'] not in unique_slave_name:
                unique_slave_name.append(slave_desc['name'])
                acc_rst_found += 1 if slave_desc['type'] == 'acc_rst' else 0
                if acc_rst_found > 1:
                    logging.error("More than one RST Controller is not supported")
                    return False, cfg
            else:
                logging.error("Error on slave "+str(slave)+" not unique name!")
                return False, cfg
    logging.debug('Valid slave configuration')
    return True, cfg

def _validate_dma(cfg):
    dma_count = 0

    for m in cfg['masters']:
        if cfg['masters'][m]['type'] == 'acc_dma':
            dma_count += 1
    for s in cfg['slaves']:
        if cfg['slaves'][s]['type'] == 'acc_dma':
            dma_count -= 1
    return dma_count


