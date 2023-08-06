import asyncio
import tornado
from .views.base_test import BaseTest
from tinybird.csv_processing_queue import CsvChunkQueueRegistry
from tinybird.redis_client import get_redis_client
from tinybird.status import HealthChecker, REDIS_STATUS_KEY, MAX_ALLOWED_DELAY
import pytest

from .conftest import CH_ADDRESS


class StatusCheckTest(BaseTest):

    def setUp(self):
        super().setUp()

        self.redis_client = get_redis_client()
        self.redis_client.delete(REDIS_STATUS_KEY)

        self.health = None

    def tearDown(self):
        if self.health:
            self.health.terminate()
            CsvChunkQueueRegistry.get_or_create().wait_for_queue()
        super().tearDown()

    def test_should_return_initial(self):
        self.health = HealthChecker(
            hosts=[
                'http://localhost:8123',
                'http://localhost:8124'
            ],
            redis_client=self.redis_client
        )
        self.assertEqual(len(self.health.status.items()), 2)
        self.assertTrue(all(v == 'initial' for k, v in self.health.status.items()))

    def test_should_restore_status(self):
        self.health = HealthChecker(
            hosts=[
                'http://localhost:8123',
                'http://localhost:8124'
            ],
            redis_client=self.redis_client
        )
        self.health.status['http://localhost:8123'] = 'timeout'
        self.health.persist_status(self.health.status)
        health = HealthChecker(
            hosts=[
                'http://localhost:8123',
                'http://localhost:8124'
            ],
            redis_client=self.redis_client
        )
        self.assertEqual(len(health.status.items()), 2)
        self.assertEqual(health.status['http://localhost:8123'], 'timeout')

    def test_should_set_as_timeout(self):
        self.health = HealthChecker(
            hosts=[
                'http://localhost:8123',
                'http://localhost:8124'
            ],
            redis_client=self.redis_client
        )
        self.health.timings['http://localhost:8123'].append({
            'timestmap': 0,
            'elapsed': -1,
            'replication_delay': -1,
            'error': 'timeout'
        })

        new_status = self.health.hosts_status()
        self.assertEqual(new_status['http://localhost:8123'], 'timeout')

    def test_should_set_as_max_replication_delay(self):
        self.health = HealthChecker(
            hosts=[
                'http://localhost:8123',
                'http://localhost:8124'
            ],
            redis_client=self.redis_client
        )
        self.health.timings['http://localhost:8123'].append({
            'timestmap': 0,
            'elapsed': 0.01,
            'replication_delay': MAX_ALLOWED_DELAY + 1,
            'error': None
        })

        new_status = self.health.hosts_status()
        self.assertEqual(new_status['http://localhost:8123'], 'max_replication_delay')

    def test_status_should_not_go_to_ok(self):
        health = HealthChecker(
            hosts=[
                'http://localhost:8123',
                'http://localhost:8124'
            ],
            redis_client=self.redis_client
        )
        health.status['http://localhost:8123'] = 'timeout'
        health.timings['http://localhost:8123'].append({
            'timestmap': 0,
            'elapsed': 0.01,
            'replication_delay': 0,
            'error': None
        })
        new_status = health.hosts_status()
        self.assertEqual(new_status['http://localhost:8123'], 'ready_to_sync')

    @pytest.mark.skip("Skipping because it's flaky, waiting to drop support.")
    @tornado.testing.gen_test
    async def test_check_status(self):

        INVALID_HOST = 'http://invalid:8123'
        self.health = HealthChecker(
            hosts=[
                CH_ADDRESS,
                INVALID_HOST
            ],
            redis_client=self.redis_client,
            check_interval=1.0
        )
        self.health.start()
        tries = 5
        while tries:
            status = self.health.remote_status()
            if status and status[CH_ADDRESS] != 'initial':
                self.assertTrue(CH_ADDRESS in status)
                self.assertEqual(status[CH_ADDRESS], 'ok')
                self.assertTrue(INVALID_HOST in status)
                self.assertEqual(status[INVALID_HOST], 'timeout')
                self.health.terminate()
                return
            tries -= 1
            await asyncio.sleep(0.2)
        self.health.terminate()
        raise Exception("failed to check")

    def test_change_states(self):
        INVALID_HOST = 'http://invalid:8123'
        self.health = HealthChecker(
            hosts=[
                CH_ADDRESS,
                INVALID_HOST
            ],
            redis_client=self.redis_client,
            check_interval=1.0
        )
        self.health.start()
        self.health.change_status(CH_ADDRESS, 'timeout')
        self.assertEqual(self.health.remote_status()[CH_ADDRESS], 'timeout')
        self.health.change_status(CH_ADDRESS, 'ok')
        self.assertEqual(self.health.remote_status()[CH_ADDRESS], 'ok')

    def test_log_status_musnt_raise_indexerror_on_empty_timings(self):
        health = HealthChecker(
            hosts=[
                'http://localhost:8123',
                'http://localhost:8124'
            ],
            redis_client=self.redis_client
        )
        new_status = health.hosts_status()

        health.log_status(new_status)

        self.assertEqual(health.status_log, [])
