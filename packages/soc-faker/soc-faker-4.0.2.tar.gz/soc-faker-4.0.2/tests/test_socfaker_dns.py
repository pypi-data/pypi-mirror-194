def test_socfaker_dns_record(socfaker_fixture):
    assert socfaker_fixture.dns.record

def test_socfaker_dns_header_flags(socfaker_fixture):
    assert socfaker_fixture.dns.header_flags
    assert isinstance(socfaker_fixture.dns.header_flags, list)

def test_socfaker_dns_id(socfaker_fixture):
    assert socfaker_fixture.dns.id

def test_socfaker_dns_response_code(socfaker_fixture):
    assert socfaker_fixture.dns.response_code

def test_socfaker_dns_op_code(socfaker_fixture):
    assert socfaker_fixture.dns.op_code

def test_socfaker_dns_answers(socfaker_fixture):
    assert socfaker_fixture.dns.answers
    assert isinstance(socfaker_fixture.dns.answers, list)

def test_socfaker_dns_question(socfaker_fixture):
    assert socfaker_fixture.dns.question
    assert isinstance(socfaker_fixture.dns.question, dict)

def test_socfaker_dns_direction(socfaker_fixture):
    assert socfaker_fixture.dns.direction

def test_socfaker_dns_name(socfaker_fixture):
    assert socfaker_fixture.dns.name