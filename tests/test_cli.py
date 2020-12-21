import pytest

from pgbackup import cli

@pytest.fixture
def parser():
	return cli.create_parser()

url = "postgres://bob:password@example.com:5432/db_one"

def test_parser_without_driver(parser):
    """
    Without a specified driver the parser will exit
    """
    with pytest.raises(SystemExit):
         parser.parse_args([url])

def test_parser_with_driver(parser):
    """
    The parser will exit if the driver is found
    without destination
    """
    with pytest.raises(SystemExit):
        parser.parse_args([url, "--driver","local"])

def test_parser_with_driver_and_dest(parser):
    """
    The parser will not exit if it receives driver
    with destination
    """
    args= parser.parse_args([url, "--driver", "local","/some/path"])
    assert args.url == url
    assert args.driver == "local"
    assert args.destination == "/some/path"

def test_parser_with_unknown_driver(parser):
    """
    The parser will exit if the driver name is unknown
    """
    with pytest.raises(SystemExit):
        assert parser.parse_args([url, "--driver","azure",  "destination"])

def test_parser_with_known_driver(parser):
    """
    The parser will not exit if the driver name is known
    """
    for driver in ['local', 's3']:
        assert parser.parse_args([url, "--driver", driver,  "destination"])
