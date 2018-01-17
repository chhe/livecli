class LiveurlError(Exception):
    """Any error caused by Livecli will be caught
       with this exception."""


class PluginError(LiveurlError):
    """Plugin related error."""


class NoStreamsError(LiveurlError):
    def __init__(self, url):
        self.url = url
        err = "No streams found on this URL: {0}".format(url)
        Exception.__init__(self, err)


class NoPluginError(PluginError):
    """No relevant plugin has been loaded."""


class StreamError(LiveurlError):
    """Stream related error."""


__all__ = ["LiveurlError", "PluginError", "NoPluginError",
           "NoStreamsError", "StreamError"]
