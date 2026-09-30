import unittest, subprocess
from cleanup import cleanup
class CleanupTest(unittest.TestCase):
 def test_kill_timeout(self):
  calls=[];result={'defaults_before': {'sink':'original'}}
  def terminate():
   calls.append('terminate');raise subprocess.TimeoutExpired('wineserver',10)
  cleanup(terminate,lambda:calls.append('unload'),lambda:{'sink':'original'},lambda r:calls.append('write'),result)
  self.assertEqual(calls,['terminate','unload','write']);self.assertTrue(result['defaults_unchanged']);self.assertEqual(result['cleanup_errors'][0]['stage'],'terminate')
 def test_all_cleanup_errors_still_record(self):
  calls=[];result={'defaults_before': {}}
  def bad(): raise OSError('injected')
  cleanup(bad,bad,bad,lambda r:calls.append(dict(r)),result)
  self.assertEqual(len(calls),1);self.assertEqual(len(calls[0]['cleanup_errors']),3)
if __name__=='__main__':unittest.main()
