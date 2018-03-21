import unittest


from livecli.plugin.plugin import stream_weight, parse_params


class TestPluginStream(unittest.TestCase):
    def test_parse_params(self):
        self.assertEqual(
            dict(verify=False, params=dict(key="a value")),
            parse_params("""verify=False params={'key': 'a value'}""")
        )
        self.assertEqual(
            dict(verify=False),
            parse_params("""verify=False""")
        )
        self.assertEqual(
            dict(conn=['B:1', 'S:authMe', 'O:1', 'NN:code:1.23', 'NS:flag:ok', 'O:0']),
            parse_params(""""conn=['B:1', 'S:authMe', 'O:1', 'NN:code:1.23', 'NS:flag:ok', 'O:0']""")
        )

    def test_stream_weight(self):
        self.assertEqual(
            (720, "pixels"),
            stream_weight("720p"))
        self.assertEqual(
            (721, "pixels"),
            stream_weight("720p+"))
        self.assertEqual(
            (780, "pixels"),
            stream_weight("720p60"))

        self.assertTrue(
            stream_weight("720p+") > stream_weight("720p"))
        self.assertTrue(
            stream_weight("720p") == stream_weight("720p"))
        self.assertTrue(
            stream_weight("720p_3000k") > stream_weight("720p_2500k"))
        self.assertTrue(
            stream_weight("720p60_3000k") > stream_weight("720p_3000k"))
        self.assertTrue(
            stream_weight("720p_3000k") < stream_weight("720p+_3000k"))

        self.assertTrue(
            stream_weight("3000k") > stream_weight("2500k"))
        self.assertTrue(
            stream_weight("3000k") > stream_weight("3000k_alt"))
        self.assertTrue(
            stream_weight("3000k_alt") > stream_weight("3000k_alt2"))
        self.assertTrue(
            stream_weight("3000k_alt2") > stream_weight("3000k_alt4"))
