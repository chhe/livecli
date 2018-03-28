import pkgutil
import unittest

import imp
import six
from livecli import Livecli

import livecli.plugins
import os.path


class PluginTestMeta(type):
    def __new__(mcs, name, bases, dict):
        plugin_path = os.path.dirname(livecli.plugins.__file__)
        plugins = []
        for loader, pname, ispkg in pkgutil.iter_modules([plugin_path]):
            file, pathname, desc = imp.find_module(pname, [plugin_path])
            module = imp.load_module(pname, file, pathname, desc)
            if hasattr(module, "__plugin__"):
                plugins.append((pname))

        session = Livecli()

        def gentest(pname):
            def load_plugin_test(self):
                # Reset file variable to ensure it is still open when doing
                # load_plugin else python might open the plugin source .py
                # using ascii encoding instead of utf-8.
                # See also open() call here: imp._HackedGetData.get_data
                file, pathname, desc = imp.find_module(pname, [plugin_path])
                session.load_plugin(pname, file, pathname, desc)

            return load_plugin_test

        for pname in plugins:
            dict['test_{0}_load'.format(pname)] = gentest(pname)

        return type.__new__(mcs, name, bases, dict)


# Python 2.7 and Python 3
# https://pythonhosted.org/six/#six.add_metaclass
@six.add_metaclass(PluginTestMeta)
class TestPlugins(unittest.TestCase):
    """
    Test that an instance of each plugin can be created.
    """
