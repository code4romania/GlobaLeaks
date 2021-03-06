from distutils.version import StrictVersion # pylint: disable=no-name-in-module,import-error

from twisted.internet.defer import inlineCallbacks, succeed

from globaleaks.settings import GLSettings
from globaleaks.jobs.update_check_sched import UpdateCheckJob
from globaleaks.tests import helpers

packages="Package: globaleaks\n" \
         "Version: 0.0.1\n" \
         "Filename: xenial/globaleaks_1.0.0_all.deb\n\n" \
         "Version: 1.0.0\n" \
         "Filename: xenial/globaleaks_1.0.0_all.deb\n\n" \
         "Version: 1.2.3\n" \
         "Filename: xenial/globaleaks_1.0.0_all.deb\n\n" \
         "Version: 2.0.666\n" \
         "Filename: xenial/globaleaks_2.0.9_all.deb\n\n" \
         "Version: 2.0.1337\n" \
         "Filename: xenial/globaleaks_2.0.100_all.deb"


class TestExitNodesRefresh(helpers.TestGL):
    @inlineCallbacks
    def test_refresh_works(self):
        GLSettings.memory_copy.anonymize_outgoing_connections = False
        GLSettings.appstate.latest_version = '0.0.1'

        def fetch_packages_file_mock(self):
            return succeed(packages)

        UpdateCheckJob.fetch_packages_file = fetch_packages_file_mock

        yield UpdateCheckJob().operation()

        self.assertEqual(GLSettings.appstate.latest_version, '2.0.1337')
