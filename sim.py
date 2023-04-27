""" SPDX-License-Identifier: Apache-2.0 """
import argparse
import json
import logging
import logging.config
import time

from PyBoltz.Boltz import Boltz
import yaml

"""
Copyright 2023 XIA LLC, All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

""" sim.py
A wrapper for the PyBoltz package to make it usable and output the information we want.
"""

GAS_MAP = {
    "CF4": 1,
    "Argon": 2,
    "Helium-4": 3,
    "Helium-3": 4,
    "Neon": 5,
    "Krypton": 6,
    "Xenon": 7,
    "CH4": 8,
    "Ethane": 9,
    "Propane": 10,
    "Isobutane": 11,
    "CO2": 12,
    "H2O": 14,
    "Oxygen": 15,
    "Nitrogen": 16,
    "Hydrogen": 21,
    "Deuterium": 22,
    "DME": 25,
}

ANGULAR_MODEL_MAP = {
    "Okhrimvoskky": 2,
    "Capitelli Longo": 1,
    "Isotropic Scattering": 0
}


def config_boltz(cfg, obj):
    """
    Handles configuration of the Boltz object from the configuration dictionary.
    :param cfg: The dictionary containing the Boltz configuration.
    :param obj: The Boltz object that we want to configure.
    :return:
    """
    obj.NumberOfGases = len(cfg['gas']['mix'])
    gas_ids = [0] * 6
    gas_fractions = [0] * 6

    for idx, (gas, frac) in enumerate(cfg['gas']['mix'].items()):
        gas_ids[idx] = GAS_MAP[gas]
        gas_fractions[idx] = frac

    if not (0 <= sum(gas_fractions) <= 100):
        raise ValueError("Gas fractions must total to 100%.")

    obj.GasIDs = gas_ids
    obj.GasFractions = gas_fractions

    if cfg['enable_penning']:
        obj.Enable_Penning = 1
    else:
        obj.Enable_Penning = 0

    if cfg['electron']['thermal_motion']:
        obj.Enable_Thermal_Motion = 1
    else:
        obj.Enable_Thermal_Motion = 0

    obj.MaxNumberOfCollisions = cfg['events']
    obj.Max_Electron_Energy = cfg['electron']['max_energy']
    obj.TemperatureCentigrade = cfg['gas']['temperature']
    obj.Pressure_Torr = cfg['gas']['pressure']
    obj.EField = cfg['electric_field']
    obj.BField_Mag = cfg['magnetic_field']['magnitude']
    obj.BField_Angle = cfg['magnetic_field']['angle']
    obj.Console_Output_Flag = cfg['console_output']
    obj.Steady_State_Threshold = cfg['steady_state_threshold']
    obj.Which_Angular_Model = ANGULAR_MODEL_MAP[cfg['angular_model']]

    if cfg['seed'] == 0:
        seed = time.time()
    else:
        seed = cfg['seed']
    obj.Random_Seed = round(seed)


def output_results(cfg, ofile, boltz):
    """

    :param boltz:
    :return:
    """
    results = {
        "gas": {
            "mix": cfg['gas']['mix'],
            "temperature": boltz.TemperatureCentigrade,
            "pressure": boltz.Pressure_Torr,
            "ionization_rate_1_per_cm": boltz.IonisationRate,
            "attachment_rate_1_per_cm": boltz.AttachmentRate
        },
        "electric_field": boltz.EField,
        "electron": {
            "energy": {
                "value_eV": boltz.MeanElectronEnergy,
                "error_percent": boltz.MeanElectronEnergyError
            },
            "drift_velocity": {
                "x": {
                    "value_mm_per_mus": boltz.VelocityX,
                    "error_percent": boltz.VelocityErrorX
                },
                "y": {
                    "value_mm_per_mus": boltz.VelocityY,
                    "error_percent": boltz.VelocityErrorY
                },
                "z": {
                    "value_mm_per_mus": boltz.VelocityZ,
                    "error_percent": boltz.VelocityErrorZ
                }
            },
            "mean_collision_time_ps": boltz.MeanCollisionTime
        },
        "diffusion": {
            "transverse": {
                "value_cm2_per_s": boltz.TransverseDiffusion,
                "error_percent": boltz.TransverseDiffusionError,
            },
            "longitudinal": {
                "value_cm2_per_s": boltz.LongitudinalDiffusion,
                "error_percent": boltz.LongitudinalDiffusionError
            },
            "x": {
                "value_cm2_per_s": boltz.DiffusionX,
                "error_percent": boltz.ErrorDiffusionX
            },
            "y": {
                "value_cm2_per_s": boltz.DiffusionY,
                "error_percent": boltz.ErrorDiffusionY
            },
            "z": {
                "value_cm2_per_s": boltz.DiffusionZ,
                "error_percent": boltz.ErrorDiffusionZ
            },
            "yz": {
                "value_cm2_per_s": boltz.DiffusionYZ,
                "error_percent": boltz.ErrorDiffusionYZ
            },
            "xy": {
                "value_cm2_per_s": boltz.DiffusionXY,
                "error_percent": boltz.ErrorDiffusionXY
            },
            "xz": {
                "value_cm2_per_s": boltz.DiffusionXZ,
                "error_percent": boltz.ErrorDiffusionXZ
            }
        }
    }
    with open(ofile, "w") as out:
        json.dump(results, out, indent=4)


def main(args):
    """
    :param args: The command line arguments obtained from argparse.
    :return: None
    """
    with open(args.cfg, 'r', encoding='utf-8') as cfg_file:
        cfg = yaml.safe_load(cfg_file)

    logging.config.dictConfig(cfg['logging'])
    logger = logging.getLogger()

    try:
        boltz = Boltz()
        logger.info("Starting to configure the Boltz object.")
        config_boltz(cfg, boltz)
        logger.info("Starting simulation. This may take a while...")
        boltz.Start()
        logger.info("Simulation finished.")
        logger.info("Outputting the results to file.")
        output_results(cfg, args.output, boltz)
    except ValueError as verr:
        logger.error(verr)
    finally:
        pass


if __name__ == '__main__':
    try:
        PARSER = argparse.ArgumentParser(description='Wrapper for the PyBoltz package.')
        PARSER.add_argument('cfg', type=str, nargs='?',
                            help='The configuration file containing the inputs.')
        PARSER.add_argument('output', type=str, nargs='?',
                            help='The name of the output file to hold the results.')
        ARGS = PARSER.parse_args()
        main(ARGS)
    except KeyboardInterrupt:
        logging.getLogger().info("Received keyboard interrupt. Stopping execution.")
    finally:
        logging.getLogger().info("Finished execution.")
