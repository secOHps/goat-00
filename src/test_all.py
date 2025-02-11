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
#    Module: test
#
#    Description:  This file is used to define tests for unittest
#
#                           ***** UNCLASSIFIED *****
###############################################################################
import unittest
import inspect
from auto.app import *

class TestMethodDeclarations(unittest.TestCase):
    def test_expected_staticmethods_are_static(self):
        self.assertEqual(isinstance(inspect.getattr_static(UI, "print_prompt"), staticmethod), True)
        self.assertEqual(isinstance(inspect.getattr_static(UI, "print_info"), staticmethod), True)
        self.assertEqual(isinstance(inspect.getattr_static(AutoController, "assign"), staticmethod), True)
        self.assertEqual(isinstance(inspect.getattr_static(AutoController, "check_items"), staticmethod), True)
        self.assertEqual(isinstance(inspect.getattr_static(AutoController, "check_items_as_divisor"), staticmethod), True)
        self.assertEqual(isinstance(inspect.getattr_static(AutoController, "make_calculation"), staticmethod), True)
        self.assertEqual(isinstance(inspect.getattr_static(Director, "run_program"), staticmethod), True)
        self.assertEqual(isinstance(inspect.getattr_static(Director, "get_entry"), staticmethod), True)
        self.assertEqual(isinstance(inspect.getattr_static(Director, "get_all_entries"), staticmethod), True)
        self.assertEqual(isinstance(inspect.getattr_static(Director, "make_calculations"), staticmethod), True)
        self.assertEqual(isinstance(inspect.getattr_static(Utils, "format_decimal"), staticmethod), True)
        self.assertEqual(isinstance(inspect.getattr_static(Utils, "payments_left_this_year"), staticmethod), True)
        self.assertEqual(isinstance(inspect.getattr_static(Utils, "make_two_way_trip"), staticmethod), True)

class TestValueAssignments(unittest.TestCase):
    def setUp(self):
        self.auto = Auto()
        self.bad_values = [
                None,
                False,
                -1,
                '\' ',
                '_#$&',
                '',
                ' ',
                ]

    def test_constants_meet_expected_values(self):
        self.assertEqual(Constants.COST_PAYMENT, 'COST_PAYMENT')
        self.assertEqual(Constants.REMAINING_PAYMENTS, 'REMAINING_PAYMENTS')
        self.assertEqual(Constants.MILES_WORKDAY, 'MILES_WORKDAY')
        self.assertEqual(Constants.FREQ_WORKDAY, 'FREQ_WORKDAY')
        self.assertEqual(Constants.FREQ_WORKWEEK, 'FREQ_WORKWEEK')
        self.assertEqual(Constants.MILES_WEEKEND, 'MILES_WEEKEND')
        self.assertEqual(Constants.MILES_ADDITIONAL, 'MILES_ADDITIONAL')
        self.assertEqual(Constants.MPG, 'MPG')
        self.assertEqual(Constants.COST_FUEL_GALLON, 'COST_FUEL_GALLON')
        self.assertEqual(Constants.COST_ROUTINE_CAR_WASH, 'COST_ROUTINE_CAR_WASH')
        self.assertEqual(Constants.FREQ_ROUTINE_CAR_WASH, 'FREQ_ROUTINE_CAR_WASH')
        self.assertEqual(Constants.COST_ROUTINE_SERVICE, 'COST_ROUTINE_SERVICE')
        self.assertEqual(Constants.FREQ_ROUTINE_SERVICE, 'FREQ_ROUTINE_SERVICE')
        self.assertEqual(Constants.COST_ROUTINE_TIRES, 'COST_ROUTINE_TIRES')
        self.assertEqual(Constants.FREQ_ROUTINE_TIRES, 'FREQ_ROUTINE_TIRES')
        self.assertEqual(Constants.COST_ANNUAL_NON_ROUTINE, 'COST_ANNUAL_NON_ROUTINE')
        self.assertEqual(Constants.COST_INSURANCE, 'COST_INSURANCE')
        self.assertEqual(Constants.FREQ_INSURANCE, 'FREQ_INSURANCE')
        self.assertEqual(Constants.SKIPPING_PROMPT, 'SKIPPING_PROMPT')
        self.assertEqual(Constants.DEFAULT_VAL_DECIMAL, 'DEFAULT_VAL_DECIMAL')
        self.assertEqual(Constants.DEFAULT_VAL_MAXIMUM, 'DEFAULT_VAL_MAXIMUM')
        self.assertEqual(Constants.CALC_ANNUAL_PAYMENT, 'CALC_ANNUAL_PAYMENT')
        self.assertEqual(Constants.CALC_ANNUAL_MILES_DRIVEN, 'CALC_ANNUAL_MILES_DRIVEN')
        self.assertEqual(Constants.CALC_ANNUAL_FUEL, 'CALC_ANNUAL_FUEL')
        self.assertEqual(Constants.CALC_ANNUAL_CAR_WASH, 'CALC_ANNUAL_CAR_WASH')
        self.assertEqual(Constants.CALC_ANNUAL_ROUTINE_SERVICE, 'CALC_ANNUAL_ROUTINE_SERVICE')
        self.assertEqual(Constants.CALC_ANNUAL_ROUTINE_TIRES, 'CALC_ANNUAL_ROUTINE_TIRES')
        self.assertEqual(Constants.CALC_ANNUAL_NON_ROUTINE, 'CALC_ANNUAL_NON_ROUTINE')
        self.assertEqual(Constants.CALC_ANNUAL_INSURANCE, 'CALC_ANNUAL_INSURANCE')
        self.assertEqual(Constants.CALC_ANNUAL_COST_PER_MILE, 'CALC_ANNUAL_COST_PER_MILE')
        self.assertEqual(Constants.CALC_ANNUAL_OVERALL_COST, 'CALC_ANNUAL_OVERALL_COST')
        self.assertEqual(Constants.MONTHS_IN_A_YEAR, 'MONTHS_IN_A_YEAR')
        self.assertEqual(Constants.TRIPS_IN_TWO_WAY_TRIP, 'TRIPS_IN_TWO_WAY_TRIP')
        self.assertEqual(Constants.WEEKS_IN_A_YEAR, 'WEEKS_IN_A_YEAR')

    def test_values_not_empty_and_not_negative(self):
        # When attempting to assign a cost of 0, it should return 0...
        self.assertEqual(AutoController.assign(self.auto, Constants.COST_PAYMENT, 0.00, True), 0)
        # ...not a positve number...
        self.assertNotEqual(AutoController.assign(self.auto, Constants.COST_PAYMENT, 0.00, True), 1)
        # ...nor None
        self.assertNotEqual(AutoController.assign(self.auto, Constants.COST_PAYMENT, 0.00, True), None)
        # Decimals should be assigned correctly...
        self.assertEqual(AutoController.assign(self.auto, Constants.COST_PAYMENT, 3.17, True), 3.17)
        self.assertEqual(AutoController.assign(self.auto, Constants.COST_PAYMENT, "3.37", True), 3.37)
        # ...including rejecting bad'uns
        self.assertEqual(AutoController.assign(self.auto, Constants.COST_PAYMENT, ".3.37", True), 0)
        for bad_value in self.bad_values: 
            # When attempting to assign a bad value, it should default to 0...
            self.assertEqual(AutoController.assign(self.auto, Constants.COST_PAYMENT, bad_value, True), 0)
            # ...not None.
            self.assertNotEqual(AutoController.assign(self.auto, Constants.COST_PAYMENT, bad_value, True), None)

    def test_value_assignment_fails_if_referencing_wrong_property(self):
        # When attempted to assign to a non-existent property, it should return None...
        self.assertEqual(AutoController.assign(self.auto, 'NONEXISTENT_PROPERTY', 30.00), None)
        # ...not False.
        self.assertNotEqual(AutoController.assign(self.auto, 'NONEXISTENT_PROPERTY', 30.00), False)

class TestAutoController(unittest.TestCase):
    def setUp(self):
        self.auto = Auto()

    def test_calculations_will_not_run_if_no_valid_auto_class(self):
        self.assertEqual(AutoController.make_calculation(None, Constants.CALC_ANNUAL_INSURANCE), None)

    def test_calculations_will_not_run_if_not_defined(self):
        self.assertEqual(AutoController.make_calculation(self.auto, 'PRETEND_CALCULATION'), None)
        self.assertEqual(AutoController.make_calculation(self.auto, None), None)

    def test_check_items_working_correctly(self):
        self.assertEqual(AutoController.check_items(None, None), False)
        self.assertEqual(AutoController.check_items(self.auto, None), False)
        self.assertEqual(AutoController.check_items(None, []), False)
        self.assertEqual(AutoController.check_items(None, []), False)
        self.assertEqual(AutoController.check_items(self.auto, [Constants.COST_PAYMENT, Constants.REMAINING_PAYMENTS]), False)
        self.setUp_good()
        self.assertEqual(AutoController.check_items(self.auto, [Constants.COST_PAYMENT, Constants.REMAINING_PAYMENTS]), True)
        self.assertEqual(AutoController.check_items(self.auto, Constants.COST_ROUTINE_CAR_WASH), True)

    def test_check_items_as_divisor_working_correctly(self):
        self.assertEqual(AutoController.check_items_as_divisor(None, None), False)
        self.assertEqual(AutoController.check_items_as_divisor(self.auto, None), False)
        self.assertEqual(AutoController.check_items_as_divisor(None, []), False)
        self.assertEqual(AutoController.check_items_as_divisor(None, []), False)
        self.assertEqual(AutoController.check_items_as_divisor(self.auto, [Constants.COST_PAYMENT, Constants.REMAINING_PAYMENTS]), False)
        self.setUp_good()
        self.assertEqual(AutoController.check_items_as_divisor(self.auto, [Constants.COST_PAYMENT, Constants.REMAINING_PAYMENTS]), True)
        self.assertEqual(AutoController.check_items_as_divisor(self.auto, Constants.COST_ROUTINE_CAR_WASH), True)
        self.setUp_bad()
        # Make sure we catch division by zero
        self.assertEqual(AutoController.check_items_as_divisor(self.auto, Constants.MPG), False)

    def test_valid_calculations_working_correctly(self):
        self.setUp_good()
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_PAYMENT), 3677.16)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_MILES_DRIVEN), 12460)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_FUEL), 1712.70)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_CAR_WASH), 45.00)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_ROUTINE_SERVICE), 274.10)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_ROUTINE_TIRES), 197.28)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_NON_ROUTINE), 1600)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_INSURANCE), 968.04)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_COST_PER_MILE), 0.68)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_OVERALL_COST), 8474.28)

    def test_invalid_calculations_working_correctly(self):
        self.setUp_bad()
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_PAYMENT), 0)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_MILES_DRIVEN), 0)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_FUEL), None)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_CAR_WASH), 0)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_ROUTINE_SERVICE), None)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_ROUTINE_TIRES), None)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_NON_ROUTINE), 0)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_INSURANCE), None)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_COST_PER_MILE), None)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_OVERALL_COST), None)
        self.setUp_ugly()
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_PAYMENT), 0)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_MILES_DRIVEN), 0)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_FUEL), None)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_CAR_WASH), 0)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_ROUTINE_SERVICE), None)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_ROUTINE_TIRES), None)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_NON_ROUTINE), 0)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_INSURANCE), 0)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_COST_PER_MILE), None)
        self.assertEqual(AutoController.make_calculation(self.auto, Constants.CALC_ANNUAL_OVERALL_COST), None)

    def setUp_good(self):
        AutoController.assign(self.auto, Constants.COST_PAYMENT, '306.43', True)
        AutoController.assign(self.auto, Constants.REMAINING_PAYMENTS, '36', True)
        AutoController.assign(self.auto, Constants.MILES_WORKDAY, '17.8', True)
        AutoController.assign(self.auto, Constants.FREQ_WORKDAY, '5', True)
        AutoController.assign(self.auto, Constants.FREQ_WORKWEEK, '50', True)
        AutoController.assign(self.auto, Constants.MILES_WEEKEND, '30', True)
        AutoController.assign(self.auto, Constants.MILES_ADDITIONAL, '2000', True)
        AutoController.assign(self.auto, Constants.MPG, '28.3', True)
        AutoController.assign(self.auto, Constants.COST_FUEL_GALLON, '3.89', True)
        AutoController.assign(self.auto, Constants.COST_ROUTINE_CAR_WASH, '9.00', True)
        AutoController.assign(self.auto, Constants.FREQ_ROUTINE_CAR_WASH, '5', True)
        AutoController.assign(self.auto, Constants.COST_ROUTINE_SERVICE, '109.99', True)
        AutoController.assign(self.auto, Constants.FREQ_ROUTINE_SERVICE, '5000', True)
        AutoController.assign(self.auto, Constants.COST_ROUTINE_TIRES, '950.00', True)
        AutoController.assign(self.auto, Constants.FREQ_ROUTINE_TIRES, '60000', True)
        AutoController.assign(self.auto, Constants.COST_ANNUAL_NON_ROUTINE, 1600, True)
        AutoController.assign(self.auto, Constants.COST_INSURANCE, '484.02', True)
        AutoController.assign(self.auto, Constants.FREQ_INSURANCE, '2', True)

    def setUp_bad(self):
        AutoController.assign(self.auto, Constants.COST_PAYMENT, '306.43', True)
        AutoController.assign(self.auto, Constants.REMAINING_PAYMENTS, '0', True)
        AutoController.assign(self.auto, Constants.MILES_WORKDAY, '17.8', True)
        AutoController.assign(self.auto, Constants.FREQ_WORKDAY, '0', True)
        AutoController.assign(self.auto, Constants.FREQ_WORKWEEK, 4000, True)
        AutoController.assign(self.auto, Constants.MILES_WEEKEND, '0', True)
        AutoController.assign(self.auto, Constants.MILES_ADDITIONAL, 0, True)
        AutoController.assign(self.auto, Constants.MPG, '0', True)
        AutoController.assign(self.auto, Constants.COST_FUEL_GALLON, '3.89', True)
        AutoController.assign(self.auto, Constants.COST_ROUTINE_CAR_WASH, '9.00', True)
        AutoController.assign(self.auto, Constants.FREQ_ROUTINE_CAR_WASH, '0', True)
        AutoController.assign(self.auto, Constants.COST_ROUTINE_SERVICE, '109.99', True)
        AutoController.assign(self.auto, Constants.FREQ_ROUTINE_SERVICE, '0', True)
        AutoController.assign(self.auto, Constants.COST_ROUTINE_TIRES, '950.00', True)
        AutoController.assign(self.auto, Constants.FREQ_ROUTINE_TIRES, '0', True)
        AutoController.assign(self.auto, Constants.COST_ANNUAL_NON_ROUTINE, -1, True)
        AutoController.assign(self.auto, Constants.COST_INSURANCE, '484.02', True)
        AutoController.assign(self.auto, Constants.FREQ_INSURANCE, '-2', True)

    def setUp_ugly(self):
        AutoController.assign(self.auto, Constants.COST_PAYMENT, None, True)
        AutoController.assign(self.auto, Constants.REMAINING_PAYMENTS, None, True)
        AutoController.assign(self.auto, Constants.MILES_WORKDAY, None, True)
        AutoController.assign(self.auto, Constants.FREQ_WORKDAY, None, True)
        AutoController.assign(self.auto, Constants.FREQ_WORKWEEK, None, True)
        AutoController.assign(self.auto, Constants.MILES_WEEKEND, None, True)
        AutoController.assign(self.auto, Constants.MILES_ADDITIONAL, None, True)
        AutoController.assign(self.auto, Constants.MPG, None, True)
        AutoController.assign(self.auto, Constants.COST_FUEL_GALLON, None, True)
        AutoController.assign(self.auto, Constants.COST_ROUTINE_CAR_WASH, None, True)
        AutoController.assign(self.auto, Constants.FREQ_ROUTINE_CAR_WASH, None, True)
        AutoController.assign(self.auto, Constants.COST_ROUTINE_SERVICE, None, True)
        AutoController.assign(self.auto, Constants.FREQ_ROUTINE_SERVICE, None, True)
        AutoController.assign(self.auto, Constants.COST_ROUTINE_TIRES, None, True)
        AutoController.assign(self.auto, Constants.FREQ_ROUTINE_TIRES, None, True)
        AutoController.assign(self.auto, Constants.COST_ANNUAL_NON_ROUTINE, None, True)
        AutoController.assign(self.auto, Constants.COST_INSURANCE, None, True)
        AutoController.assign(self.auto, Constants.FREQ_INSURANCE, None, True)

class TestUI(unittest.TestCase):
    def setUp(self):
        self.bad_values = [
                None,
                False,
                True,
                -1,
                '\' ',
                '_#$&',
                '',
                ' ',
                'PRETEND_PROMPT',
                ]

    def test_prompts_print_successfully(self):
        self.assertTrue(UI.print_prompt(Constants.COST_PAYMENT, True))
        self.assertTrue(UI.print_prompt(Constants.REMAINING_PAYMENTS, True))
        self.assertTrue(UI.print_prompt(Constants.MILES_WORKDAY, True))
        self.assertTrue(UI.print_prompt(Constants.FREQ_WORKDAY, True))
        self.assertTrue(UI.print_prompt(Constants.FREQ_WORKWEEK, True))
        self.assertTrue(UI.print_prompt(Constants.MILES_WEEKEND, True))
        self.assertTrue(UI.print_prompt(Constants.MILES_ADDITIONAL, True))
        self.assertTrue(UI.print_prompt(Constants.MPG, True))
        self.assertTrue(UI.print_prompt(Constants.COST_FUEL_GALLON, True))
        self.assertTrue(UI.print_prompt(Constants.COST_ROUTINE_CAR_WASH, True))
        self.assertTrue(UI.print_prompt(Constants.FREQ_ROUTINE_CAR_WASH, True))
        self.assertTrue(UI.print_prompt(Constants.COST_ROUTINE_SERVICE, True))
        self.assertTrue(UI.print_prompt(Constants.FREQ_ROUTINE_SERVICE, True))
        self.assertTrue(UI.print_prompt(Constants.COST_ROUTINE_TIRES, True))
        self.assertTrue(UI.print_prompt(Constants.FREQ_ROUTINE_TIRES, True))
        self.assertTrue(UI.print_prompt(Constants.COST_ANNUAL_NON_ROUTINE, True))
        self.assertTrue(UI.print_prompt(Constants.COST_INSURANCE, True))
        self.assertTrue(UI.print_prompt(Constants.FREQ_INSURANCE, True))
        self.assertTrue(UI.print_prompt(Constants.SKIPPING_PROMPT, True))

    def test_infos_print_successfully(self):
        self.assertTrue(UI.print_info(Constants.CALC_ANNUAL_PAYMENT, 0, True))
        self.assertTrue(UI.print_info(Constants.CALC_ANNUAL_MILES_DRIVEN, 0, True))
        self.assertTrue(UI.print_info(Constants.CALC_ANNUAL_FUEL, 0, True))
        self.assertTrue(UI.print_info(Constants.CALC_ANNUAL_CAR_WASH, 0, True))
        self.assertTrue(UI.print_info(Constants.CALC_ANNUAL_ROUTINE_SERVICE, 0, True))
        self.assertTrue(UI.print_info(Constants.CALC_ANNUAL_ROUTINE_TIRES, 0, True))
        self.assertTrue(UI.print_info(Constants.CALC_ANNUAL_NON_ROUTINE, 0, True))
        self.assertTrue(UI.print_info(Constants.CALC_ANNUAL_INSURANCE, 0, True))
        self.assertTrue(UI.print_info(Constants.CALC_ANNUAL_COST_PER_MILE, 0, True))
        self.assertTrue(UI.print_info(Constants.CALC_ANNUAL_OVERALL_COST, 0, True))

    def test_bad_prompts_do_not_print(self):
        for bad_value in self.bad_values: 
            self.assertFalse(UI.print_prompt(bad_value))

    def test_bad_infos_do_not_print(self):
        for bad_value in self.bad_values: 
            self.assertFalse(UI.print_info(bad_value, 0))

class TestDirector(unittest.TestCase):
    def setUp(self):
        self.auto = Auto()

    def test_exits_if_no_auto_class(self):
        self.assertTrue(Director.run_program(None, True), True)

    def test_able_to_handle_valid_entries(self):
        # It shouldn't accept invalid entries...
        self.assertEqual(Director.get_entry(self.auto, None, True), None)
        self.assertEqual(Director.get_entry(self.auto, 'PRETEND_ENTRY', True), None)
        # ...but should accept valid ones
        self.assertNotEqual(Director.get_entry(self.auto, Constants.COST_PAYMENT, True), None)
        self.assertNotEqual(Director.get_entry(self.auto, Constants.REMAINING_PAYMENTS, True), None)
        self.assertNotEqual(Director.get_entry(self.auto, Constants.MILES_WORKDAY, True), None)
        self.assertNotEqual(Director.get_entry(self.auto, Constants.FREQ_WORKDAY, True), None)
        self.assertNotEqual(Director.get_entry(self.auto, Constants.FREQ_WORKWEEK, True), None)
        self.assertNotEqual(Director.get_entry(self.auto, Constants.MILES_WEEKEND, True), None)
        self.assertNotEqual(Director.get_entry(self.auto, Constants.MILES_ADDITIONAL, True), None)
        self.assertNotEqual(Director.get_entry(self.auto, Constants.MPG, True), None)
        self.assertNotEqual(Director.get_entry(self.auto, Constants.COST_FUEL_GALLON, True), None)
        self.assertNotEqual(Director.get_entry(self.auto, Constants.COST_ROUTINE_CAR_WASH, True), None)
        self.assertNotEqual(Director.get_entry(self.auto, Constants.FREQ_ROUTINE_CAR_WASH, True), None)
        self.assertNotEqual(Director.get_entry(self.auto, Constants.COST_ROUTINE_SERVICE, True), None)
        self.assertNotEqual(Director.get_entry(self.auto, Constants.FREQ_ROUTINE_SERVICE, True), None)
        self.assertNotEqual(Director.get_entry(self.auto, Constants.COST_ROUTINE_TIRES, True), None)
        self.assertNotEqual(Director.get_entry(self.auto, Constants.FREQ_ROUTINE_TIRES, True), None)
        self.assertNotEqual(Director.get_entry(self.auto, Constants.COST_ANNUAL_NON_ROUTINE, True), None)
        self.assertNotEqual(Director.get_entry(self.auto, Constants.COST_INSURANCE, True), None)
        self.assertNotEqual(Director.get_entry(self.auto, Constants.FREQ_INSURANCE, True), None)

    def test_will_not_run_entries_on_invalid_auto_class(self):
        self.assertEqual(Director.get_all_entries(None), None)
        
    def test_will_not_make_calculations_on_invalid_auto_class(self):
        self.assertEqual(Director.make_calculations(None, True), None)

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.bad_values = [
                None,
                "PRETEND_STUFF",
                -1,
                '',
                ' ',
                ]
    def test_decimals_format_successfully(self):
        # None should evaluate to None...
        self.assertEqual(Utils.format_decimal(None), None)
        # ..and so should empty.
        self.assertEqual(Utils.format_decimal(''), None)
        self.assertEqual(Utils.format_decimal(' '), None)
        # True should evaluate to decimal...
        self.assertEqual(Utils.format_decimal(True), 1)
        # ...and so should False.
        self.assertEqual(Utils.format_decimal(False), 0)
        # It shouldn't let us try to parse stuff with more than one decimal point
        self.assertEqual(Utils.format_decimal('#%*Y@FSDFJ:2an8.fasd8.dff39ljh'), None)
        self.assertEqual(Utils.format_decimal('192.168.0.1'), None)
        self.assertEqual(Utils.format_decimal('.90.00'), None)
        # It should return None if we try just a string...
        self.assertEqual(Utils.format_decimal('I\'m just a lonely string.'), None)
        # ..or just a decimal point.
        self.assertEqual(Utils.format_decimal('.'), None)
        # We're killing any numbers of a ridiculous size...no ones car costs that much...
        self.assertEqual(Utils.format_decimal('999999999999.01'), None)
        # ...but let's make sure the maximum value still succeeds.
        self.assertEqual(Utils.format_decimal('999999999999'), 999_999_999_999)
        # Everything else should parse down to the expected format...
        self.assertEqual(Utils.format_decimal('#%*Y@FSDFJ:2an8.fasd8dff39ljh'), 28.84)
        self.assertEqual(Utils.format_decimal('nafju10g'), 10.00)
        self.assertEqual(Utils.format_decimal('$416.49'), 416.49)
        self.assertEqual(Utils.format_decimal('10.428428'), 10.43)
        self.assertEqual(Utils.format_decimal('10999'), 10999)
        self.assertEqual(Utils.format_decimal('1'), 1)
        self.assertEqual(Utils.format_decimal('0'), 0)
        # ...including if we actually pass a float or an int.
        self.assertEqual(Utils.format_decimal(123456789), 123456789)
        self.assertEqual(Utils.format_decimal(1234567.89), 1234567.89)
        self.assertEqual(Utils.format_decimal(1234.56789), 1234.57)
        self.assertEqual(Utils.format_decimal(1.006), 1.01)
        self.assertEqual(Utils.format_decimal(1.00), 1)
        self.assertEqual(Utils.format_decimal(0.00), 0)
        self.assertEqual(Utils.format_decimal(0.9), 0.90)
        self.assertEqual(Utils.format_decimal(0.09), 0.09)
        self.assertEqual(Utils.format_decimal(0.009), 0.01)
        self.assertEqual(Utils.format_decimal(0.0009), 0)
        self.assertEqual(Utils.format_decimal(0.004), 0)
        self.assertEqual(Utils.format_decimal(0.005), 0.01)
        self.assertEqual(Utils.format_decimal(0.000000000009), 0)
        self.assertEqual(Utils.format_decimal(1), 1)
        self.assertEqual(Utils.format_decimal(0), 0)

    def test_payments_left_this_year_calculate_correctly(self):
        for bad_value in self.bad_values:
            self.assertEqual(Utils.make_two_way_trip(bad_value), None)
        self.assertEqual(Utils.payments_left_this_year(15323), 12)
        self.assertEqual(Utils.payments_left_this_year(13), 12)
        self.assertEqual(Utils.payments_left_this_year(12.49), 12)
        self.assertEqual(Utils.payments_left_this_year(11.5), 12)
        self.assertEqual(Utils.payments_left_this_year(11.49), 11)
        self.assertEqual(Utils.payments_left_this_year(12), 12)
        self.assertEqual(Utils.payments_left_this_year(8), 8)
        self.assertEqual(Utils.payments_left_this_year(1), 1)
        self.assertEqual(Utils.payments_left_this_year(0), 0)

    def test_two_way_trip_calculates_correctly(self):
        for bad_value in self.bad_values:
            self.assertEqual(Utils.make_two_way_trip(bad_value), None)
        self.assertEqual(Utils.make_two_way_trip(0), 0)
        self.assertEqual(Utils.make_two_way_trip("3"), 6)
        self.assertEqual(Utils.make_two_way_trip(19.94), 39.88)

    def test_annualize_weekly_miles_calculates_correctly(self):
        for bad_value in self.bad_values:
            self.assertEqual(Utils.annualize_weekly_miles(bad_value), None)
        self.assertEqual(Utils.annualize_weekly_miles(0), 0)
        self.assertEqual(Utils.annualize_weekly_miles(1), 52)
        self.assertEqual(Utils.annualize_weekly_miles(843.6), 43867.2)

