"""
Test for response helper.

Note that it is expected to use the right datatypes for the parameters.
"""

import pytest
from src.utils.response_helper import ResponseHelper


@pytest.fixture
def sut():
    """SUT for unittest."""
    return ResponseHelper()


@pytest.mark.unit
class TestUnitResponseHelper:
    """Unit test for response helper."""

    @pytest.mark.parametrize(
        "kwargs, exp_response, exp_status",
        [
            (
                {"message": "test message", "data": "test"},
                {"status": "success", "data": "test", "message": "test message"},
                200,
            ),
            (
                {"message": "test message", "status": 202},
                {"status": "success", "message": "test message"},
                202,
            ),
            ({}, {"status": "success"}, 200),
        ],
    )
    def test_success_response(self, sut, kwargs, exp_response, exp_status):
        response, status = sut.success_response(**kwargs)

        assert response == exp_response and status == exp_status

    @pytest.mark.parametrize(
        "kwargs, exp_response, exp_status",
        [
            (
                {"message": "test message", "details": "test details"},
                {
                    "status": "error",
                    "error": {
                        "message": "test message",
                        "details": "test details",
                        "code": 400,
                    },
                },
                400,
            ),
            (
                {"message": "test message", "errorcode": 404},
                {"status": "error", "error": {"message": "test message", "code": 404}},
                404,
            ),
            ({}, {"status": "error", "error": {"code": 400}}, 400),
        ],
    )
    def test_error_response(self, sut, kwargs, exp_response, exp_status):
        response, status = sut.error_response(**kwargs)

        assert response == exp_response and status == exp_status

    @pytest.mark.parametrize(
        "details, exp_response",
        [
            (
                None,
                {
                    "status": "error",
                    "error": {
                        "code": 500,
                        "message": "Unknown server error, try again.",
                    },
                },
            ),
            (
                "test detail",
                {
                    "status": "error",
                    "error": {
                        "code": 500,
                        "message": "Unknown server error, try again.",
                        "details": "test detail",
                    },
                },
            ),
        ],
    )
    def test_unkown_error(self, sut, details, exp_response):
        response, status = sut.unkown_error(details)

        assert response == exp_response and status == 500
