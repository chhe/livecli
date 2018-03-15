from livecli.stream import HTTPStream


def _get_streams(session):
    return dict(support=HTTPStream(session, "http://test.se/support"))
