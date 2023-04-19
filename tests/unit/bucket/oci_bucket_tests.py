# import re
# import unittest

# from base_crawler.bucket.oci_bucket import OracleBucketManager
# from tests import test_helper


# class OciBucketTests(unittest.TestCase):

#     def setUp(self):
#         self.bucket_client = OracleBucketManager()
#         self.file_content = test_helper.read_test_file("test_file.txt")
#         self.file_name = "test_file.txt"

#     def test_should_create_put_bucket_request_successfully(self):
#         request = self.bucket_client.create_put_bucket_request(
#             file_content=self.file_content, file_name=self.file_name, callback=None, errback=None)

#         self.assertRegex(request._get_url(),
#                         re.compile(r"/Coleta/test_file.txt"))

#     def test_should_raise_exception_when_required_kwarg_does_not_exist(self):
#         with self.assertRaises(KeyError):
#             _ = self.bucket_client.create_put_bucket_request(
#                 file_name=self.file_name, callback=None, errback=None)


# if __name__ == "__main__":
#     unittest.main()
