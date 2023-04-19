""" SPDX-License-Identifier: Apache-2.0 """
import argparse
from PyBoltz.Boltz import Boltz

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

"""


def main():
    boltz = Boltz()

    # Set the number of gases
    boltz.NumberOfGases = 2
    # Set the number of collisons
    boltz.MaxNumberOfCollisions = 1 * 40000000.0
    # Set penning
    boltz.Enable_Penning = 0
    # Calculate the electron energy
    boltz.Enable_Thermal_Motion = 1
    boltz.Max_Electron_Energy = 0.0
    # Set the gas's with their given number
    boltz.GasIDs = [2, 8, 0, 0, 0, 0]
    # Set the gas fractions
    boltz.GasFractions = [90, 10, 0, 0, 0, 0]
    # Set the temperature
    boltz.TemperatureCentigrade = 23.
    # Set the pressure
    boltz.Pressure_Torr = 750.062
    # Set the electric field
    # boltz.EField = ap.root.CH4["10.0"].Reduced_Field[5]
    # Set the magnetic field and angle
    boltz.BField_Mag = 0
    boltz.BField_Angle = 0
    boltz.Console_Output_Flag = 0
    boltz.Steady_State_Threshold = 40
    boltz.Which_Angular_Model = 2

    boltz.Start()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Received keyboard interrupt. Stopping execution.")
    finally:
        print("Finished execution.")
