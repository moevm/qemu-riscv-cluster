# Tests
- the project uses unit and integration tests to verify the work of the project
- the test settings are stored in the ``pytest.ini`` file, which is located in the root of the project

## Unit tets
Unit tests are contained in the unit folder, where each file contains tests of individual functions or classes.

There are several ways to run tests:
- unit tests only ``pytest -m unit``
- run a specific text file ``pytest test_payload_generator.py``

## Integration tests
Integration tests are located in the integration folder, which contains tests that test the interaction of different classes and entities.

The file ``conftest.py`` is used for storing general fixtures.

There are several ways to run tests:
- unit tests only ``pytest -m integration``
- run a specific text file ``pytest test_grpc_payload_generator.py``

it is possible to run all the tests with the command ``pytest`` from the root directory.