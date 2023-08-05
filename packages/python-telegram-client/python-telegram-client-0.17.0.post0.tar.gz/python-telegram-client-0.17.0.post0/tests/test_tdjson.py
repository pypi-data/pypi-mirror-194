from unittest.mock import Mock, patch

from teleclient.tdjson import _get_tdjson_lib_path


class TestGetTdjsonTdlibPath:
    def test_for_darwin(self):
        mocked_system = Mock(return_value='Darwin')
        mocked_resource = Mock()
        mocked_find_library = Mock(return_value=None)

        with patch('teleclient.tdjson.platform.system', mocked_system):
            with patch('teleclient.tdjson.pkg_resources.resource_filename', mocked_resource):
                with patch('teleclient.tdjson.ctypes.util.find_library', mocked_find_library):
                    _get_tdjson_lib_path()

        mocked_resource.assert_called_once_with('teleclient', 'lib/darwin/libtdjson.dylib')

    def test_for_linux(self):
        mocked_system = Mock(return_value='Linux')
        mocked_resource = Mock(return_value='/tmp/')
        mocked_find_library = Mock(return_value=None)

        with patch('teleclient.tdjson.platform.system', mocked_system):
            with patch('teleclient.tdjson.pkg_resources.resource_filename', mocked_resource):
                with patch('teleclient.tdjson.ctypes.util.find_library', mocked_find_library):
                    _get_tdjson_lib_path()

        mocked_resource.assert_called_once_with('teleclient', 'lib/linux/libtdjson.so')

    def test_for_windows(self):
        mocked_system = Mock(return_value='Windows')
        mocked_resource = Mock(return_value='/tmp/')
        mocked_find_library = Mock(return_value=None)

        with patch('teleclient.tdjson.platform.system', mocked_system):
            with patch('teleclient.tdjson.pkg_resources.resource_filename', mocked_resource):
                with patch('teleclient.tdjson.ctypes.util.find_library', mocked_find_library):
                    _get_tdjson_lib_path()

        mocked_resource.assert_called_once_with('teleclient', 'lib/linux/libtdjson.so')

    def test_unknown(self):
        mocked_system = Mock(return_value='Unknown')
        mocked_resource = Mock(return_value='/tmp/')
        mocked_find_library = Mock(return_value=None)

        with patch('teleclient.tdjson.platform.system', mocked_system):
            with patch('teleclient.tdjson.pkg_resources.resource_filename', mocked_resource):
                with patch('teleclient.tdjson.ctypes.util.find_library', mocked_find_library):
                    _get_tdjson_lib_path()

        mocked_resource.assert_called_once_with('teleclient', 'lib/linux/libtdjson.so')
