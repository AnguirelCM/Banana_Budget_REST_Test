import requests
import unittest
import json
import random

def check_response_for(response_json, cost_expected):
    response_Data = json.loads(response_json)
    return response_Data["totalCost"] == cost_expected

def check_response_error(response_json, error_expected):
    response_Data = json.loads(response_json)
    return response_Data["error"] == error_expected

class BobsBananaBudgetTest(unittest.TestCase):

    def setUp(self):
        self.url = "https://bananabudget.azurewebsites.net/"

    def test_GET_Request_as_URL(self):
        response = requests.get(self.url+"?startDate=10-1-2000&numberOfDays=7")
        self.assertEqual(200, response.status_code)
        self.assertTrue(check_response_for(response.content, "$0.25"))

    def test_GET_Request_as_Params(self):
        params = {"startDate":"10-1-2000", "numberOfDays":"7"}
        response = requests.get(self.url, params=params)
        self.assertEqual(200, response.status_code)
        self.assertTrue(check_response_for(response.content, "$0.25"))

    def test_GET_minimum_days_weekday_first_7(self):
        params = {"startDate":"8-1-2018", "numberOfDays":"1"}
        response = requests.get(self.url, params=params)
        self.assertEqual(200, response.status_code)
        self.assertTrue(check_response_for(response.content, "$0.05"))

    def test_GET_minimum_days_weekend_first_7(self):
        params = {"startDate":"7-1-2017", "numberOfDays":"1"}
        response = requests.get(self.url, params=params)
        self.assertEqual(200, response.status_code)
        self.assertTrue(check_response_for(response.content, "$0.00"))

    def test_GET_minimum_days_weekday_second_7(self):
        params = {"startDate":"8-8-2018", "numberOfDays":"1"}
        response = requests.get(self.url, params=params)
        self.assertEqual(200, response.status_code)
        self.assertTrue(check_response_for(response.content, "$0.10"))

    def test_GET_minimum_days_weekday_third_7(self):
        params = {"startDate":"8-15-2018", "numberOfDays":"1"}
        response = requests.get(self.url, params=params)
        self.assertEqual(200, response.status_code)
        self.assertTrue(check_response_for(response.content, "$0.15"))

    def test_GET_minimum_days_weekday_fourth_7(self):
        params = {"startDate":"8-22-2018", "numberOfDays":"1"}
        response = requests.get(self.url, params=params)
        self.assertEqual(200, response.status_code)
        self.assertTrue(check_response_for(response.content, "$0.20"))

    def test_GET_minimum_days_weekday_fifth_7(self):
        params = {"startDate":"8-29-2018", "numberOfDays":"1"}
        response = requests.get(self.url, params=params)
        self.assertEqual(200, response.status_code)
        self.assertTrue(check_response_for(response.content, "$0.25"))

    def test_GET_month_roll_over(self):
        params = {"startDate":"8-29-2018", "numberOfDays":"7"}
        response = requests.get(self.url, params=params)
        self.assertEqual(200, response.status_code)
        self.assertTrue(check_response_for(response.content, "$0.85"))

    def test_GET_first_7_days_with_random_month_and_year(self):
        randomYear = random.randint(0,10000)
        randomMonth = random.randint(1,12)
        response = requests.get(self.url + "?startDate="+str(randomMonth)+"-1-"+str(randomYear)+"&numberOfDays=7")
        self.assertEqual(200, response.status_code)
        self.assertTrue(check_response_for(response.content, "$0.25"))

    def test_GET_second_7_days_with_random_month_and_year(self):
        randomYear = random.randint(0,10000)
        randomMonth = random.randint(1,12)
        response = requests.get(self.url + "?startDate="+str(randomMonth)+"-8-"+str(randomYear)+"&numberOfDays=7")
        self.assertEqual(200, response.status_code)
        self.assertTrue(check_response_for(response.content, "$0.50"))

    def test_GET_third_7_days_with_random_month_and_year(self):
        randomYear = random.randint(0,10000)
        randomMonth = random.randint(1,12)
        response = requests.get(self.url + "?startDate="+str(randomMonth)+"-15-"+str(randomYear)+"&numberOfDays=7")
        self.assertEqual(200, response.status_code)
        self.assertTrue(check_response_for(response.content, "$0.75"))

    def test_GET_fourth_7_days_with_random_month_and_year(self):
        randomYear = random.randint(0,10000)
        randomMonth = random.randint(1,12)
        response = requests.get(self.url + "?startDate="+str(randomMonth)+"-22-"+str(randomYear)+"&numberOfDays=7")
        self.assertEqual(200, response.status_code)
        self.assertTrue(check_response_for(response.content, "$1.00"))

    def test_GET_maximum_days(self):
        params = {"startDate":"7-1-2017", "numberOfDays":"365"}
        response = requests.get(self.url, params=params)
        self.assertEqual(200, response.status_code)
        # ToDo: This needs to be manually calculated -- for the purposes of this code test, I assumed the value it sent back was correct
        self.assertTrue(check_response_for(response.content, "$35.00"))

    def test_GET_under_minimum_days(self):
        params = {"startDate":"7-1-2017", "numberOfDays":"0"}
        response = requests.get(self.url, params=params)
        self.assertEqual(400, response.status_code)
        self.assertTrue(check_response_error(response.content, "Invalid numberOfDays"))

    def test_GET_over_maximum_days(self):
        # This test fails, as the end point allows more days than the maximum I was given
        params = {"startDate":"7-1-2017", "numberOfDays":"366"}
        response = requests.get(self.url, params=params)
        self.assertEqual(400, response.status_code)
        self.assertTrue(check_response_error(response.content, "Invalid numberOfDays"))

    def test_GET_improper_date(self):
        params = {"startDate":"13-1-2017", "numberOfDays":"10"}
        response = requests.get(self.url, params=params)
        self.assertEqual(400, response.status_code)
        self.assertTrue(check_response_error(response.content, "Invalid startDate"))

    def test_POST(self):
        params = {"startDate":"8-1-2018", "numberOfDays":"1"}
        response = requests.post(self.url, data=params)
        self.assertEqual(404, response.status_code)
        self.assertRegex(response.text, 'Cannot POST')

    def test_PUT(self):
        params = {"startDate":"8-1-2018", "numberOfDays":"1"}
        response = requests.put(self.url, data=params)
        self.assertEqual(404, response.status_code)
        self.assertRegex(response.text, 'Cannot PUT')

    def test_DELETE(self):
        response = requests.delete(self.url)
        self.assertEqual(404, response.status_code)
        self.assertRegex(response.text, 'Cannot DELETE')

if __name__ == "__main__":
    unittest.main()