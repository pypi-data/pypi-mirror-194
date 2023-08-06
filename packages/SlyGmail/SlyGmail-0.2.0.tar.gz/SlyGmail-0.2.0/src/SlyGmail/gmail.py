"""
GMail API and types
"""
from dataclasses import dataclass
import os.path

from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes

import aiofiles

from SlyAPI import *

class Scope:
    GMail         = 'https://mail.google.com/'
    GMailSend     = 'https://www.googleapis.com/auth/gmail.send'
    GMailReadOnly = 'https://www.googleapis.com/auth/gmail.readonly'

EMAIL_HEADERS = {'Content-Type': 'message/rfc822'}

def _encode_attachment(content: bytes, filename: str):
    content_type, encoding = mimetypes.guess_type(filename)
    # gmail does not like attaching .zip file names
    # filename should not include any path
    filename = os.path.split(filename)[1].replace('.zip', '.zip.attachment')
    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)

    match main_type:
        case 'text':
            msg = MIMEText(str(content, encoding='utf8'), sub_type)
        case 'image':
            msg = MIMEImage(content, sub_type)
        case 'audio':
            msg = MIMEAudio(content, sub_type)
        case _:
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(content)

    msg.add_header('Content-Disposition', 'attachment', filename=filename)

    return msg

@dataclass
class Email:
    to: str
    sender: str
    subject: str
    body: str
    attachments: list[str|tuple[bytes, str]] # filepath | (content, filename)

    async def encoded(self) -> str:

        if not self.attachments:
            message = MIMEText(self.body)
            message['to'] = self.to
            message['from'] = self.sender
            message['subject'] = self.subject
        else:
            message = MIMEMultipart()
            message['to'] = self.to
            message['from'] = self.sender
            message['subject'] = self.subject

            message.attach(MIMEText(self.body))

            for attachment in self.attachments:
                
                if isinstance(attachment, tuple):
                    content, filename = attachment
                else:
                    async with aiofiles.open(attachment, 'rb') as f:
                        content = await f.read()
                    filename = attachment

                msg = _encode_attachment(content, filename)

                message.attach(msg)

        return message.as_string()


class Gmail(WebAPI):
    """Gmail API Client"""
    base_url = "https://gmail.googleapis.com/upload/gmail/v1/"

    def __init__(self, auth: OAuth2):
        super().__init__(auth)

    async def send(self, to: str, subject: str, body: str, attachments: list[str|tuple[bytes, str]] | None = None, from_email: str='me'):
        if attachments is None:
            attachments = []
        email = Email(to, from_email, subject, body, attachments)
        return await self._users_messages_send(email)

    async def _users_messages_send(self, email: Email):

        data = await email.encoded()

        if email.attachments:
            params = {'uploadType': 'multipart'}
        else:
            params = {}
        
        return await self.post_form(
            F"users/{email.sender}/messages/send",
            params, data=data, headers=EMAIL_HEADERS
            )

