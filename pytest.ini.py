[pytest]
addopts = -v -s --alluredir=allure-results --strict-markers
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    smoke: дымовые тесты
    regression: регрессионные тесты
