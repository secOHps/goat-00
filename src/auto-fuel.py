###############################################################################
#                           ***** UNCLASSIFIED *****
# Copyright 2023 Modern Technology Solutions, Inc. Alexandria, Virginia
#
# This material is subject to export controls imposed by the United States Export
# Administration Act of 1979, as amended and the International Traffic In Arms
# Regulation (ITAR), 22 CFR 120-130
# *******************************************************************************
#
#    File:  auto-fuel.py
#
#    Description:  This file is the entrypoint into the Auto Fuel and Maintenance app
#
#                           ***** UNCLASSIFIED *****
###############################################################################
from auto.app import *

if not Director.run_program():
    print("Something went wrong. Exiting.")
else:
    print("Thank you for letting us help you calculate your auto costs. Exiting.")
quit()
