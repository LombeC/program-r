import unittest
import unittest.mock
from datetime import datetime

from apscheduler.events import SchedulerEvent, JobEvent, JobSubmissionEvent, JobExecutionEvent

from programr.scheduling.scheduler import ProgramrScheduler, scheduled

from programrtest.aiml_tests.client import TestClient


class MockScheduler(object):

    def __init__(self):
        self._started = False
        self._emptied = False
        self._jobs = {}

    def start(self, *args, **kwargs):
        self._started = True

    def shutdown(self, wait=True):
        self._started = False

    def add_job(self, func, trigger=None, args=None, kwargs=None, id=None, name=None,
                misfire_grace_time=None, coalesce=None, max_instances=None,
                next_run_time=None, jobstore='default', executor='default',
                replace_existing=False, **trigger_args):
        self._jobs[id] = id

    def get_job(self, job_id, jobstore=None):
        if job_id in self._jobs:
            return self._jobs[job_id]
        return None

    def remove_job(self, job_id, jobstore=None):
        del self._jobs[job_id]

    def remove_all_jobs(self):
        self._emptied = True
        self._jobs.clear()


class MockProgramrScheduler(ProgramrScheduler):

    def __init__(self, client, config):
        self._scheduled = False
        ProgramrScheduler.__init__(self, client, config)

    def _create_scheduler(self):
        return MockScheduler()

    def scheduled(self, userid, clientid, action, text):
        self._scheduled = True


class ProgramrSchedulerTests(unittest.TestCase):

    def setUp(self):
        self._test_client = TestClient()
        ProgramrScheduler.schedulers.clear()
        self.assertEquals(0, len(ProgramrScheduler.schedulers.keys()))

    def create_config(self, remove, debug, listeners, name="Scheduler1"):
        config = unittest.mock.Mock()
        config.remove_all_jobs = remove
        config.debug_level = debug
        config.add_listeners = listeners
        config.name = name
        return config

    def test_registration(self):

        scheduler1 = MockProgramrScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(ProgramrScheduler.schedulers)
        self.assertEquals(1, len(ProgramrScheduler.schedulers.keys()))
        self.assertTrue("Scheduler1" in ProgramrScheduler.schedulers)
        self.assertEquals(scheduler1, ProgramrScheduler.schedulers['Scheduler1'])

        scheduler2 = MockProgramrScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(ProgramrScheduler.schedulers)
        self.assertEquals(1, len(ProgramrScheduler.schedulers.keys()))
        self.assertTrue("Scheduler1" in ProgramrScheduler.schedulers)
        self.assertEquals(scheduler1, ProgramrScheduler.schedulers['Scheduler1'])

        scheduler3 = MockProgramrScheduler(self._test_client, self.create_config(False, None, False, name="Scheduler3"))
        self.assertIsNotNone(ProgramrScheduler.schedulers)
        self.assertEquals(2, len(ProgramrScheduler.schedulers.keys()))
        self.assertTrue("Scheduler1" in ProgramrScheduler.schedulers)
        self.assertTrue("Scheduler3" in ProgramrScheduler.schedulers)
        self.assertEquals(scheduler1, ProgramrScheduler.schedulers['Scheduler1'])
        self.assertEquals(scheduler3, ProgramrScheduler.schedulers['Scheduler3'])

    def test_start_stop(self):
        scheduler = MockProgramrScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertFalse(scheduler._scheduler._started)
        scheduler.start()
        self.assertTrue(scheduler._scheduler._started)
        scheduler.stop()
        self.assertFalse(scheduler._scheduler._started)

    def test_empty_jobs(self):
        scheduler = MockProgramrScheduler(self._test_client, self.create_config(True, None, False))
        self.assertIsNotNone(scheduler)
        self.assertTrue(scheduler._scheduler._emptied)
        self.assertEquals(0, len(scheduler._scheduler._jobs.keys()))

    def test_not_empty_jobs(self):
        scheduler = MockProgramrScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertFalse(scheduler._scheduler._emptied)
        self.assertEquals(0, len(scheduler._scheduler._jobs.keys()))

    def test_add_job_every_seconds(self):
        scheduler = MockProgramrScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertEquals(0, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_seconds("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEquals(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_seconds("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEquals(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_seconds("testuser", "testclient", "MESSAGE", "REMIND ME 2", 3)
        self.assertEquals(2, len(scheduler._scheduler._jobs.keys()))

    def test_add_job_every_minutes(self):
        scheduler = MockProgramrScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertEquals(0, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_minutes("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEquals(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_minutes("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEquals(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_minutes("testuser", "testclient", "MESSAGE", "REMIND ME 2", 3)
        self.assertEquals(2, len(scheduler._scheduler._jobs.keys()))

    def test_add_job_every_hours(self):
        scheduler = MockProgramrScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertEquals(0, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_hours("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEquals(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_hours("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEquals(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_hours("testuser", "testclient", "MESSAGE", "REMIND ME 2", 3)
        self.assertEquals(2, len(scheduler._scheduler._jobs.keys()))

    def test_add_job_every_days(self):
        scheduler = MockProgramrScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertEquals(0, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_days("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEquals(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_days("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEquals(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_days("testuser", "testclient", "MESSAGE", "REMIND ME 2", 3)
        self.assertEquals(2, len(scheduler._scheduler._jobs.keys()))

    def test_add_job_every_weeks(self):
        scheduler = MockProgramrScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertEquals(0, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_weeks("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEquals(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_weeks("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEquals(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_every_n_weeks("testuser", "testclient", "MESSAGE", "REMIND ME 2", 3)
        self.assertEquals(2, len(scheduler._scheduler._jobs.keys()))

    def test_add_job_in_seconds(self):
        scheduler = MockProgramrScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertEquals(0, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_seconds("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEquals(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_seconds("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEquals(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_seconds("testuser", "testclient", "MESSAGE", "REMIND ME 2", 3)
        self.assertEquals(2, len(scheduler._scheduler._jobs.keys()))

    def test_add_job_in_minutes(self):
        scheduler = MockProgramrScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertEquals(0, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_minutes("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEquals(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_minutes("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEquals(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_minutes("testuser", "testclient", "MESSAGE", "REMIND ME 2", 3)
        self.assertEquals(2, len(scheduler._scheduler._jobs.keys()))

    def test_add_job_in_hours(self):
        scheduler = MockProgramrScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertEquals(0, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_hours("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEquals(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_hours("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEquals(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_hours("testuser", "testclient", "MESSAGE", "REMIND ME 2", 3)
        self.assertEquals(2, len(scheduler._scheduler._jobs.keys()))

    def test_add_job_in_days(self):
        scheduler = MockProgramrScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertEquals(0, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_days("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEquals(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_days("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEquals(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_days("testuser", "testclient", "MESSAGE", "REMIND ME 2", 3)
        self.assertEquals(2, len(scheduler._scheduler._jobs.keys()))

    def test_add_job_in_weeks(self):
        scheduler = MockProgramrScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertEquals(0, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_weeks("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEquals(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_weeks("testuser", "testclient", "MESSAGE", "REMIND ME", 3)
        self.assertEquals(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_in_n_weeks("testuser", "testclient", "MESSAGE", "REMIND ME 2", 3)
        self.assertEquals(2, len(scheduler._scheduler._jobs.keys()))

    def test_add_job_as_cron(self):
        scheduler = MockProgramrScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(scheduler)
        self.assertEquals(0, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_as_cron("testuser", "testclient", "MESSAGE", "REMIND ME", second='*/3')
        self.assertEquals(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_as_cron("testuser", "testclient", "MESSAGE", "REMIND ME", second='*/3')
        self.assertEquals(1, len(scheduler._scheduler._jobs.keys()))

        scheduler.schedule_as_cron("testuser", "testclient", "MESSAGE", "REMIND ME 2", second='*/3')
        self.assertEquals(2, len(scheduler._scheduler._jobs.keys()))

    def test_get_event_str_scheduler_event(self):
        event = SchedulerEvent("code", "alias")
        message = ProgramrScheduler.get_event_str(event)
        self.assertIsNotNone(message)
        self.assertEquals("SchedulerEvent [code] [alias]", message)

    def test_get_event_str_job_event(self):
        event = JobEvent ("code", "id", "jobstore")
        message = ProgramrScheduler.get_event_str(event)
        self.assertIsNotNone(message)
        self.assertEquals("JobEvent [code] [id] [jobstore] [None]", message)

    def test_get_event_str_job_submission_event(self):
        event = JobSubmissionEvent ("code", "job_id", "jobstore", [])
        message = ProgramrScheduler.get_event_str(event)
        self.assertIsNotNone(message)
        self.assertEquals("JobSubmissionEvent [code] [job_id] [jobstore] [[]]", message)

    def test_get_event_str_job_execution_event(self):
        scheduled_run_time = datetime.strptime("10/04/18 19:02", "%d/%m/%y %H:%M")
        event = JobExecutionEvent ("code", "job_id", "jobstore", scheduled_run_time, retval=1)
        message = ProgramrScheduler.get_event_str(event)
        self.assertIsNotNone(message)
        self.assertEquals("JobExecutionEvent [code] [job_id] [jobstore] [2018-04-10 19:02:00] [1]", message)

    def test_get_event_str_job_execution_event_with_exception(self):
        scheduled_run_time = datetime.strptime("10/04/18 19:02", "%d/%m/%y %H:%M")
        event = JobExecutionEvent ("code", "job_id", "jobstore", scheduled_run_time, retval=1, exception=Exception("Test Error"))
        message = ProgramrScheduler.get_event_str(event)
        self.assertIsNotNone(message)
        self.assertEquals("JobExecutionEvent [code] [job_id] [jobstore] [2018-04-10 19:02:00] [1] [Test Error]", message)

    def test_get_event_unknown(self):
        event = unittest.mock.Mock()
        message = ProgramrScheduler.get_event_str(event)
        self.assertIsNone(message)

    def test_scheduled(self):
        scheduler1 = MockProgramrScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(ProgramrScheduler.schedulers)
        self.assertEquals(1, len(ProgramrScheduler.schedulers.keys()))
        self.assertTrue("Scheduler1" in ProgramrScheduler.schedulers)
        self.assertEquals(scheduler1, ProgramrScheduler.schedulers['Scheduler1'])

        self.assertFalse(scheduler1._scheduled)
        scheduled("Scheduler1", "User1", "TestClient", "MESSAGE", "REMIND ME")
        self.assertTrue(scheduler1._scheduled)

    def test_scheduled_unknown_scheduler(self):
        scheduler1 = MockProgramrScheduler(self._test_client, self.create_config(False, None, False))
        self.assertIsNotNone(ProgramrScheduler.schedulers)
        self.assertEquals(1, len(ProgramrScheduler.schedulers.keys()))
        self.assertTrue("Scheduler1" in ProgramrScheduler.schedulers)
        self.assertEquals(scheduler1, ProgramrScheduler.schedulers['Scheduler1'])

        self.assertFalse(scheduler1._scheduled)
        scheduled("Scheduler2", "User1", "TestClient", "MESSAGE", "REMIND ME")
        self.assertFalse(scheduler1._scheduled)
