import pytest
from ai_workers.code_custodian import CodeCustodianAI

def test_code_custodian_initialization():
    custodian = CodeCustodianAI()
    assert custodian is not None
