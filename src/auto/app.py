###############################################################################
#                           ***** UNCLASSIFIED *****
# Copyright 2023 Modern Technology Solutions, Inc. Alexandria, Virginia
#
# This material is subject to export controls imposed by the United States Export
# Administration Act of 1979, as amended and the International Traffic In Arms
# Regulation (ITAR), 22 CFR 120-130
# *******************************************************************************
#
#    File:  app.py
#
#    Module: auto
#
#    Description:  This file is used to define the auto fuel and maintenance app
#
#                           ***** UNCLASSIFIED *****
###############################################################################
import re

#############
# Constants #
#############
class Constants():
    # For collecting, formatting and recording user input
    COST_PAYMENT = 'COST_PAYMENT'
    REMAINING_PAYMENTS = 'REMAINING_PAYMENTS'
    MILES_WORKDAY = 'MILES_WORKDAY'
    FREQ_WORKDAY = 'FREQ_WORKDAY'
    FREQ_WORKWEEK = 'FREQ_WORKWEEK'
    MILES_WEEKEND = 'MILES_WEEKEND'
    MPG = 'MPG'
    MILES_ADDITIONAL = 'MILES_ADDITIONAL'
    COST_FUEL_GALLON = 'COST_FUEL_GALLON'
    COST_ROUTINE_CAR_WASH = 'COST_ROUTINE_CAR_WASH'
    FREQ_ROUTINE_CAR_WASH = 'FREQ_ROUTINE_CAR_WASH'
    COST_ROUTINE_SERVICE = 'COST_ROUTINE_SERVICE'
    FREQ_ROUTINE_SERVICE = 'FREQ_ROUTINE_SERVICE'
    COST_ROUTINE_TIRES = 'COST_ROUTINE_TIRES'
    FREQ_ROUTINE_TIRES = 'FREQ_ROUTINE_TIRES'
    COST_ANNUAL_NON_ROUTINE = 'COST_ANNUAL_NON_ROUTINE'
    COST_INSURANCE = 'COST_INSURANCE'
    FREQ_INSURANCE = 'FREQ_INSURANCE'
    SKIPPING_PROMPT = 'SKIPPING_PROMPT'
    DEFAULT_VAL_DECIMAL = 'DEFAULT_VAL_DECIMAL'
    DEFAULT_VAL_MAXIMUM = 'DEFAULT_VAL_MAXIMUM'

    # For triggering system calculations
    CALC_ANNUAL_PAYMENT = 'CALC_ANNUAL_PAYMENT'
    CALC_ANNUAL_MILES_DRIVEN = 'CALC_ANNUAL_MILES_DRIVEN'
    CALC_ANNUAL_FUEL = 'CALC_ANNUAL_FUEL'
    CALC_ANNUAL_CAR_WASH = 'CALC_ANNUAL_CAR_WASH'
    CALC_ANNUAL_ROUTINE_SERVICE = 'CALC_ANNUAL_ROUTINE_SERVICE'
    CALC_ANNUAL_ROUTINE_TIRES = 'CALC_ANNUAL_ROUTINE_TIRES'
    CALC_ANNUAL_NON_ROUTINE = 'CALC_ANNUAL_NON_ROUTINE'
    CALC_ANNUAL_INSURANCE = 'CALC_ANNUAL_INSURANCE'
    CALC_ANNUAL_COST_PER_MILE = 'CALC_ANNUAL_COST_PER_MILE'
    CALC_ANNUAL_OVERALL_COST = 'CALC_ANNUAL_OVERALL_COST'

    # Misc
    MONTHS_IN_A_YEAR = 'MONTHS_IN_A_YEAR'
    TRIPS_IN_TWO_WAY_TRIP = 'TRIPS_IN_TWO_WAY_TRIP'
    WEEKS_IN_A_YEAR = 'WEEKS_IN_A_YEAR'

######
# UI #
######
class UI():
    prompts = {
            Constants.COST_PAYMENT: 'What is your monthly car payment in dollars and cents? Leave blank for none. ',
            Constants.REMAINING_PAYMENTS: 'How many car payments do you have left? ',
            Constants.MILES_WORKDAY: 'How many miles do you drive from home to work (one way)? ',
            Constants.FREQ_WORKDAY: 'How many times per week do you drive to work (one way)? ',
            Constants.FREQ_WORKWEEK: 'How many weeks per year do you drive to work? ',
            Constants.MILES_WEEKEND: 'How many additional miles total do you regularly drive per week, for things like shopping or cruising, and not including rare events like vacation? ',
            Constants.MILES_ADDITIONAL: 'How many additional miles do you drive per year for rare events such as vacation? ',
            Constants.MPG: 'How many MPG (combined) do you average? ',
            Constants.COST_FUEL_GALLON: 'What is the average fuel price per gallon over the course of a year? ',
            Constants.COST_ROUTINE_CAR_WASH: 'What does a routine car wash cost? ',
            Constants.FREQ_ROUTINE_CAR_WASH: 'How many times per year do you wash your car? ',
            Constants.COST_ROUTINE_SERVICE: 'What does routine service (e.g., oil, tire rotation) cost? ',
            Constants.FREQ_ROUTINE_SERVICE: 'How many miles do you go in between routine services? ',
            Constants.COST_ROUTINE_TIRES: 'How much do new tires cost you? ',
            Constants.FREQ_ROUTINE_TIRES: 'How many miles do you go in between tire replacements? ',
            Constants.COST_ANNUAL_NON_ROUTINE: 'Roughly how much do you spend per year on service for unexpected, non-routine issues? ',
            Constants.COST_INSURANCE: 'What is your insurance premium on this vehicle? ',
            Constants.FREQ_INSURANCE: 'How many times per year do you pay the premium? ',
            Constants.SKIPPING_PROMPT: 'Skipping prompt due to user declaration that testing is in progress...',
            }
    infos = {
            Constants.CALC_ANNUAL_MILES_DRIVEN: 'Miles driven',
            Constants.CALC_ANNUAL_PAYMENT: 'Car payment',
            Constants.CALC_ANNUAL_FUEL: 'Fuel',
            Constants.CALC_ANNUAL_CAR_WASH: 'Car wash',
            Constants.CALC_ANNUAL_ROUTINE_SERVICE: 'Routine service',
            Constants.CALC_ANNUAL_ROUTINE_TIRES: 'Routine tires',
            Constants.CALC_ANNUAL_NON_ROUTINE: 'Non-routine service',
            Constants.CALC_ANNUAL_INSURANCE: 'Insurance',
            Constants.CALC_ANNUAL_COST_PER_MILE: 'Cost per mile',
            Constants.CALC_ANNUAL_OVERALL_COST: 'Total annual cost',
            }

    @staticmethod
    def print_prompt(prompt, testing = False, silent = True):
        # Load requested prompt if we can...
        prompt = UI.prompts[prompt] if prompt in UI.prompts else None
        # ...returning False if we can't.
        if prompt is None: return False
        response = True
        # Generate a prompt, or if testing, just print it.
        if not testing:
            response = Utils.format_decimal(input(prompt))
        else:
            if not silent:
                print(UI.prompts[Constants.SKIPPING_PROMPT])
                print(prompt)
        return response

    @staticmethod
    def print_info(info, cost, testing = False):
        # Load requested calculation text if we can...
        info = UI.infos[info] if info in UI.infos else None
        # ...returning False if we can't.
        if info is None: return False
        if not testing:
            print(info)
            print(cost)
        return True

##################
# AutoController #
##################
class AutoController():
    @staticmethod
    def assign(auto, prop, val, testing = False):
        # Won't try to format a number here -- use Utils.format_decimal(), but we will exit if we get something unmanageable
        if val == None or val == '' or ((isinstance(val, int) or isinstance(val, float)) and int(val) < 0):
            val = Auto.default_values[Constants.DEFAULT_VAL_DECIMAL]
        if prop in auto.assigned_values:
            try:
                val = float(val)
                if not testing:
                    print('OK.')
            except:
                if not testing:
                    print(f'Unable to use `{val}`, changing to default of `{Auto.default_values[Constants.DEFAULT_VAL_DECIMAL]}`.')
                val = Auto.default_values[Constants.DEFAULT_VAL_DECIMAL]
            auto.assigned_values[prop] = val
            return val
        return None

    @staticmethod
    def check_items(auto, items):
        if not isinstance(items, list): items = [items]
        if auto == None or items == None or len(items) < 0: return False
        for item in items:
            if not item in auto.assigned_values or (item in auto.assigned_values and (auto.assigned_values[item] == None or auto.assigned_values[item] < 0)): return False
        return True

    @staticmethod
    def check_items_as_divisor(auto, items):
        if not isinstance(items, list): items = [items]
        if auto == None or items == None or len(items) < 0: return False
        for item in items:
            if not item in auto.assigned_values or (item in auto.assigned_values and (auto.assigned_values[item] == None or not auto.assigned_values[item] > 0)): return False
        return True

    @staticmethod
    def make_calculation(auto, calculation):
        # Won't make a calculation if we have an invalid value
        if auto == None or calculation not in Auto.calculations_to_do: return None
        match calculation:
            case Constants.CALC_ANNUAL_PAYMENT:
                if not AutoController.check_items(auto, [
                    Constants.COST_PAYMENT,
                    Constants.REMAINING_PAYMENTS,
                    ]): return None
                # Minify for readability
                a = auto.assigned_values[Constants.COST_PAYMENT]
                b = Utils.payments_left_this_year(auto.assigned_values[Constants.REMAINING_PAYMENTS])
                return round(a * b, 2)
            case Constants.CALC_ANNUAL_MILES_DRIVEN:
                if not AutoController.check_items(auto, [
                    Constants.MILES_WORKDAY,
                    Constants.FREQ_WORKDAY,
                    Constants.FREQ_WORKWEEK,
                    Constants.MILES_WEEKEND,
                    Constants.MILES_ADDITIONAL,
                    ]): return None
                # Minify for readability
                a = Utils.make_two_way_trip(auto.assigned_values[Constants.MILES_WORKDAY])
                b = auto.assigned_values[Constants.FREQ_WORKDAY]
                c = auto.assigned_values[Constants.FREQ_WORKWEEK]
                d = Utils.annualize_weekly_miles(auto.assigned_values[Constants.MILES_WEEKEND])
                e = auto.assigned_values[Constants.MILES_ADDITIONAL]
                return round((a * b * c) + d + e, 2)
            case Constants.CALC_ANNUAL_FUEL:
                if not AutoController.check_items(auto, [
                    Constants.MILES_WORKDAY,
                    Constants.FREQ_WORKDAY,
                    Constants.FREQ_WORKWEEK,
                    Constants.MILES_WEEKEND,
                    Constants.MILES_ADDITIONAL,
                    ]): return None
                if not AutoController.check_items_as_divisor(auto, [
                    Constants.COST_FUEL_GALLON,
                    Constants.MPG,
                    ]): return None

                # Minify for readability
                a = Utils.make_two_way_trip(auto.assigned_values[Constants.MILES_WORKDAY])
                b = auto.assigned_values[Constants.FREQ_WORKDAY]
                c = auto.assigned_values[Constants.FREQ_WORKWEEK]
                d = Utils.annualize_weekly_miles(auto.assigned_values[Constants.MILES_WEEKEND])
                e = auto.assigned_values[Constants.MILES_ADDITIONAL]
                f = auto.assigned_values[Constants.MPG]
                g = auto.assigned_values[Constants.COST_FUEL_GALLON]
                return round(((a * b * c) + d + e) / f * g, 2)
            case Constants.CALC_ANNUAL_CAR_WASH:
                if not AutoController.check_items(auto, [
                    Constants.COST_ROUTINE_CAR_WASH,
                    Constants.FREQ_ROUTINE_CAR_WASH,
                    ]): return None
                # Minify for readability
                a = auto.assigned_values[Constants.COST_ROUTINE_CAR_WASH]
                b = auto.assigned_values[Constants.FREQ_ROUTINE_CAR_WASH]
                return round(a * b, 2)
            case Constants.CALC_ANNUAL_ROUTINE_SERVICE:
                if not AutoController.check_items(auto, [
                    Constants.MILES_WORKDAY,
                    Constants.FREQ_WORKDAY,
                    Constants.FREQ_WORKWEEK,
                    Constants.MILES_WEEKEND,
                    Constants.MILES_ADDITIONAL,
                    ]): return None
                if not AutoController.check_items_as_divisor(auto, [
                    Constants.COST_ROUTINE_SERVICE,
                    Constants.FREQ_ROUTINE_SERVICE,
                    ]): return None
                # Minify for readability
                a = Utils.make_two_way_trip(auto.assigned_values[Constants.MILES_WORKDAY])
                b = auto.assigned_values[Constants.FREQ_WORKDAY]
                c = auto.assigned_values[Constants.FREQ_WORKWEEK]
                d = Utils.annualize_weekly_miles(auto.assigned_values[Constants.MILES_WEEKEND])
                e = auto.assigned_values[Constants.MILES_ADDITIONAL]
                f = auto.assigned_values[Constants.FREQ_ROUTINE_SERVICE]
                g = auto.assigned_values[Constants.COST_ROUTINE_SERVICE]
                return round(((a * b * c) + d + e) / f * g, 2)
            case Constants.CALC_ANNUAL_ROUTINE_TIRES:
                if not AutoController.check_items(auto, [
                    Constants.MILES_WORKDAY,
                    Constants.FREQ_WORKDAY,
                    Constants.FREQ_WORKWEEK,
                    Constants.MILES_WEEKEND,
                    Constants.MILES_ADDITIONAL,
                    ]): return None
                if not AutoController.check_items_as_divisor(auto, [
                    Constants.COST_ROUTINE_TIRES,
                    Constants.FREQ_ROUTINE_TIRES,
                    ]): return None
                # Minify for readability
                a = Utils.make_two_way_trip(auto.assigned_values[Constants.MILES_WORKDAY])
                b = auto.assigned_values[Constants.FREQ_WORKDAY]
                c = auto.assigned_values[Constants.FREQ_WORKWEEK]
                d = Utils.annualize_weekly_miles(auto.assigned_values[Constants.MILES_WEEKEND])
                e = auto.assigned_values[Constants.MILES_ADDITIONAL]
                f = auto.assigned_values[Constants.FREQ_ROUTINE_TIRES]
                g = auto.assigned_values[Constants.COST_ROUTINE_TIRES]
                return round(((a * b * c) + d + e) / f * g, 2)
            case Constants.CALC_ANNUAL_NON_ROUTINE:
                if not AutoController.check_items(auto, Constants.COST_ANNUAL_NON_ROUTINE): return None
                # Minify for readability
                a = auto.assigned_values[Constants.COST_ANNUAL_NON_ROUTINE]
                return round(a, 2)
            case Constants.CALC_ANNUAL_INSURANCE:
                if not AutoController.check_items(auto, [
                    Constants.COST_INSURANCE,
                    Constants.FREQ_INSURANCE,
                    ]): return None
                # Minify for readability
                a = auto.assigned_values[Constants.COST_INSURANCE]
                b = auto.assigned_values[Constants.FREQ_INSURANCE]
                return round(a * b, 2)
            case Constants.CALC_ANNUAL_COST_PER_MILE:
                if not AutoController.check_items(auto, [
                    Constants.COST_PAYMENT,
                    Constants.REMAINING_PAYMENTS,
                    Constants.MILES_WORKDAY,
                    Constants.FREQ_WORKDAY,
                    Constants.FREQ_WORKWEEK,
                    Constants.MILES_WEEKEND,
                    Constants.MILES_ADDITIONAL,
                    Constants.COST_ROUTINE_CAR_WASH,
                    Constants.FREQ_ROUTINE_CAR_WASH,
                    Constants.COST_ANNUAL_NON_ROUTINE,
                    Constants.COST_INSURANCE,
                    Constants.FREQ_INSURANCE,
                    ]): return None
                if not AutoController.check_items_as_divisor(auto, [
                    Constants.MPG,
                    Constants.COST_FUEL_GALLON,
                    Constants.COST_ROUTINE_SERVICE,
                    Constants.FREQ_ROUTINE_SERVICE,
                    Constants.COST_ROUTINE_TIRES,
                    Constants.FREQ_ROUTINE_TIRES,
                    ]): return None
                # Minify for readability
                ##############
                # Miles driven
                a = Utils.make_two_way_trip(auto.assigned_values[Constants.MILES_WORKDAY])
                b = auto.assigned_values[Constants.FREQ_WORKDAY]
                c = auto.assigned_values[Constants.FREQ_WORKWEEK]
                d = Utils.annualize_weekly_miles(auto.assigned_values[Constants.MILES_WEEKEND])
                e = auto.assigned_values[Constants.MILES_ADDITIONAL]
                A = (a * b * c) + d + e
                #########
                # Payment
                f = auto.assigned_values[Constants.COST_PAYMENT]
                g = Utils.payments_left_this_year(auto.assigned_values[Constants.REMAINING_PAYMENTS])
                B = f * g
                ###########
                # Fuel cost
                h = auto.assigned_values[Constants.MPG]
                i = auto.assigned_values[Constants.COST_FUEL_GALLON]
                C = A / h * i
                ##########
                # Car wash
                j = auto.assigned_values[Constants.COST_ROUTINE_CAR_WASH]
                k = auto.assigned_values[Constants.FREQ_ROUTINE_CAR_WASH]
                D = j * k
                #################
                # Routine service
                l = auto.assigned_values[Constants.FREQ_ROUTINE_SERVICE]
                m = auto.assigned_values[Constants.COST_ROUTINE_SERVICE]
                E = A / l * m
                ###############
                # Routine tires
                n = auto.assigned_values[Constants.FREQ_ROUTINE_TIRES]
                o = auto.assigned_values[Constants.COST_ROUTINE_TIRES]
                F = A / n * o
                #####################
                # Non-routine service
                G = auto.assigned_values[Constants.COST_ANNUAL_NON_ROUTINE]
                ###########
                # Insurance
                p = auto.assigned_values[Constants.COST_INSURANCE]
                q = auto.assigned_values[Constants.FREQ_INSURANCE]
                H = p * q
                ##########################################################
                # Cost per mile. Sum of annual costs / annual miles driven
                try:
                    # Catch division by zero. If ya' don't drive, you have zero cost!
                    return 0 if A <= 0 else round((B + C + D + E + F + G + H) / A, 2)
                except:
                    # For all other errors, return None to signal a more significant problem in the calculation
                    return None
            case Constants.CALC_ANNUAL_OVERALL_COST:
                if not AutoController.check_items(auto, [
                    Constants.COST_PAYMENT,
                    Constants.REMAINING_PAYMENTS,
                    Constants.MILES_WORKDAY,
                    Constants.FREQ_WORKDAY,
                    Constants.FREQ_WORKWEEK,
                    Constants.MILES_WEEKEND,
                    Constants.MILES_ADDITIONAL,
                    Constants.COST_ROUTINE_CAR_WASH,
                    Constants.FREQ_ROUTINE_CAR_WASH,
                    Constants.COST_ANNUAL_NON_ROUTINE,
                    Constants.COST_INSURANCE,
                    Constants.FREQ_INSURANCE,
                    ]): return None
                if not AutoController.check_items_as_divisor(auto, [
                    Constants.MPG,
                    Constants.COST_FUEL_GALLON,
                    Constants.COST_ROUTINE_SERVICE,
                    Constants.FREQ_ROUTINE_SERVICE,
                    Constants.COST_ROUTINE_TIRES,
                    Constants.FREQ_ROUTINE_TIRES,
                    ]): return None
                # Minify for readability
                ##############
                # Miles driven
                a = Utils.make_two_way_trip(auto.assigned_values[Constants.MILES_WORKDAY])
                b = auto.assigned_values[Constants.FREQ_WORKDAY]
                c = auto.assigned_values[Constants.FREQ_WORKWEEK]
                d = Utils.annualize_weekly_miles(auto.assigned_values[Constants.MILES_WEEKEND])
                e = auto.assigned_values[Constants.MILES_ADDITIONAL]
                A = (a * b * c) + d + e
                #########
                # Payment
                f = auto.assigned_values[Constants.COST_PAYMENT]
                g = Utils.payments_left_this_year(auto.assigned_values[Constants.REMAINING_PAYMENTS])
                B = f * g
                ###########
                # Fuel cost
                h = auto.assigned_values[Constants.MPG]
                i = auto.assigned_values[Constants.COST_FUEL_GALLON]
                C = A / h * i
                ##########
                # Car wash
                j = auto.assigned_values[Constants.COST_ROUTINE_CAR_WASH]
                k = auto.assigned_values[Constants.FREQ_ROUTINE_CAR_WASH]
                D = j * k
                #################
                # Routine service
                l = auto.assigned_values[Constants.FREQ_ROUTINE_SERVICE]
                m = auto.assigned_values[Constants.COST_ROUTINE_SERVICE]
                E = A / l * m
                ###############
                # Routine tires
                n = auto.assigned_values[Constants.FREQ_ROUTINE_TIRES]
                o = auto.assigned_values[Constants.COST_ROUTINE_TIRES]
                F = A / n * o
                #####################
                # Non-routine service
                G = auto.assigned_values[Constants.COST_ANNUAL_NON_ROUTINE]
                ###########
                # Insurance
                p = auto.assigned_values[Constants.COST_INSURANCE]
                q = auto.assigned_values[Constants.FREQ_INSURANCE]
                H = p * q
                ##########################################################
                # Overall cost per mile. Sum of annual costs / annual miles driven
                return round(B + C + D + E + F + G + H, 2)
            case _:
                return None
        return True

########
# Auto #
########
class Auto():
    default_values = {
        Constants.DEFAULT_VAL_DECIMAL: float(0),
        Constants.DEFAULT_VAL_MAXIMUM: float(999_999_999_999),
        }
    assigned_values = {}
    calculations_to_do = (
        Constants.CALC_ANNUAL_MILES_DRIVEN,
        Constants.CALC_ANNUAL_PAYMENT,
        Constants.CALC_ANNUAL_FUEL,
        Constants.CALC_ANNUAL_CAR_WASH,
        Constants.CALC_ANNUAL_ROUTINE_SERVICE,
        Constants.CALC_ANNUAL_ROUTINE_TIRES,
        Constants.CALC_ANNUAL_NON_ROUTINE,
        Constants.CALC_ANNUAL_INSURANCE,
        Constants.CALC_ANNUAL_COST_PER_MILE,
        Constants.CALC_ANNUAL_OVERALL_COST,
        )
    def __init__(self):
        self.assigned_values = {
            Constants.COST_PAYMENT: None,
            Constants.REMAINING_PAYMENTS: None,
            Constants.MILES_WORKDAY: None,
            Constants.FREQ_WORKDAY: None,
            Constants.FREQ_WORKWEEK: None,
            Constants.MILES_WEEKEND: None,
            Constants.MILES_ADDITIONAL: None,
            Constants.MPG: None,
            Constants.COST_FUEL_GALLON: None,
            Constants.COST_ROUTINE_CAR_WASH: None,
            Constants.FREQ_ROUTINE_CAR_WASH: None,
            Constants.COST_ROUTINE_SERVICE: None,
            Constants.FREQ_ROUTINE_SERVICE: None,
            Constants.COST_ROUTINE_TIRES: None,
            Constants.FREQ_ROUTINE_TIRES: None,
            Constants.COST_ANNUAL_NON_ROUTINE: None,
            Constants.COST_INSURANCE: None,
            Constants.FREQ_INSURANCE: None,
            }

############
# Director #
############
class Director():
    @staticmethod
    def run_program(auto = None, testing = False):
        auto = Auto()
        if auto == None or testing: return True
        print("Tell us about your car.")
        Director.get_all_entries(auto)
        print("ANNUAL INFO & COSTS")
        Director.make_calculations(auto)
        return True
        
    @staticmethod
    def get_entry(auto, entry, testing = False):
        if not entry in auto.assigned_values or not entry in UI.prompts:
            return None
        return AutoController.assign(auto, entry, UI.print_prompt(entry, testing), testing)

    @staticmethod
    def get_all_entries(auto):
        if auto == None: return None
        for entry in auto.assigned_values:
            Director.get_entry(auto, entry)
        return True

    @staticmethod
    def make_calculations(auto, testing = False):
        if auto == None: return None
        for calculation in auto.calculations_to_do:
            UI.print_info(calculation, AutoController.make_calculation(auto, calculation), testing)
        return True


#########
# Utils #
#########
class Utils():
    default_values = {
            Constants.MONTHS_IN_A_YEAR: 12,
            Constants.TRIPS_IN_TWO_WAY_TRIP: 2,
            Constants.WEEKS_IN_A_YEAR: 52,
            }
    @staticmethod
    def format_decimal(val):
        # We expect the format dollars.cents without a leading dollar sign, e.g. 483.03
        # If we don't have a number in that format, we'll do our best to parse the value into such a format.
        if val is not None:
            # If we already have a float or int, just round it and return it...
            if isinstance(val, int) or isinstance(val, float):
                val_new = round(float(val), 2)
                if val_new <= Auto.default_values[Constants.DEFAULT_VAL_MAXIMUM]: return val_new
            # ...but if it's a string...
            else:
                # ...our parser should handle most of the garbage we throw at it and reformat.
                try:
                    # If someone is trying to parse more than one decimal point, e.g. 842.593.5, gracefully bail.
                    if len(val.split('.')) <= 2:
                        # Strip non-digit and non-',' chars, make float, round to second place
                        val_new = round(float(re.sub(r'[^0-9.]', '', val)), 2)
                        if val_new <= Auto.default_values[Constants.DEFAULT_VAL_MAXIMUM]: return val_new
                # ...but it not, just give it a miss.
                except:
                    pass
        return None

    @staticmethod
    def payments_left_this_year(val):
        # Not going to go to a ton of validating for this simple calculation, save to ensure we have a positive number...
        # ...for anything else, just do a generic try/except and force the number into a whole number
        try:
            val = int(round(val))
            if val < 0: return None
            if val >= Utils.default_values[Constants.MONTHS_IN_A_YEAR]: 
                val = Utils.default_values[Constants.MONTHS_IN_A_YEAR]
            return val
        except:
            return None

    @staticmethod
    def make_two_way_trip(val):
        # Not going to go to a ton of validating for this simple calculation, save to ensure we have a positive number...
        try:
            val = float(val)
            if val < 0: return None
            return val * Utils.default_values[Constants.TRIPS_IN_TWO_WAY_TRIP]
        except:
            return None

    @staticmethod
    def annualize_weekly_miles(val):
        # Not going to go to a ton of validating for this simple calculation, save to ensure we have a positive number...
        try:
            val = float(val)
            if val < 0: return None
            return round(val * Utils.default_values[Constants.WEEKS_IN_A_YEAR], 2)
        except:
            return None
