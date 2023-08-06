import sys, pytest
from SlyGmail import *

@pytest.mark.skipif(sys.gettrace() is None, reason="sends real email")
async def test_readme():

    gmail = Gmail(OAuth2('test/app.json', 'test/user.json'))

    to_email = open('test/test_email.txt').read().strip()

    await gmail.send(to_email, 'test subject', 'test body')

@pytest.mark.skipif(sys.gettrace() is None, reason="sends real email")
async def test_send_attachment():

    gmail = Gmail(OAuth2('test/app.json', 'test/user.json'))

    to_email = open('test/test_email.txt').read().strip()

    await gmail.send(to_email, 'My Subject Unto You',
        """
            Hi there,

            Please see the attached test file.

            Thanks,
            Me
        """, ['test/test_attachment.txt'])