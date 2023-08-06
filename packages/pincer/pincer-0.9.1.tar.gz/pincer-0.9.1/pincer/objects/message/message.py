# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple, Union, List, Optional, TYPE_CHECKING

from aiohttp import FormData, Payload
import json
from PIL.Image import Image

from ..app.interaction_base import CallbackType
from ..guild.role import Role
from ..message.file import File
from ..message.embed import Embed
from ..message.user_message import AllowedMentionTypes
from ..user import User
from ...exceptions import CommandReturnIsEmpty
from ...utils.api_object import APIObject
from ...utils.snowflake import Snowflake

if TYPE_CHECKING:
    from ..app import InteractionFlags
    from .component import MessageComponent


@dataclass
class AllowedMentions(APIObject):
    parse: List[AllowedMentionTypes]
    roles: List[Union[Role, Snowflake]]
    users: List[Union[User, Snowflake]]
    reply: bool = True

    def to_dict(self):
        def get_str_id(obj: Union[Snowflake, User, Role]) -> str:
            if hasattr(obj, "id"):
                obj = obj.id

            return str(obj)

        return {
            "parse": self.parse,
            "roles": list(map(get_str_id, self.roles)),
            "users": list(map(get_str_id, self.users)),
            "replied_user": self.reply
        }


@dataclass
class Message:
    # TODO: Write docs
    content: str = ''
    attachments: Optional[List[File]] = None
    tts: Optional[bool] = False
    embeds: Optional[List[Embed]] = None
    allowed_mentions: Optional[AllowedMentions] = None
    components: Optional[List[MessageComponent]] = None
    flags: Optional[InteractionFlags] = None
    type: Optional[CallbackType] = None

    def __post_init__(self):

        if not self.attachments:
            return

        attch = []

        for count, value in enumerate(self.attachments):
            if isinstance(value, File):
                attch.append(value)
            elif isinstance(value, Image):
                attch.append(File.from_image(
                    value,
                    f"file{count}.png",
                ))
            elif isinstance(value, str):
                attch.append(File.from_file(value))
            else:
                raise ValueError(f"Attachment {count} is invalid type.")

        self.attachments = attch

    def to_dict(self):
        if len(self.content) < 1 and not self.embeds and not self.attachments:
            raise CommandReturnIsEmpty("Cannot return empty message.")

        allowed_mentions = (
            self.allowed_mentions.to_dict()
            if self.allowed_mentions else {}
        )

        # Attachments aren't serialized
        # because they are not sent as part of the json
        resp = {
            "content": self.content,
            "tts": self.tts,
            "flags": self.flags,
            "embeds": [embed.to_dict() for embed in (self.embeds or [])],
            "allowed_mentions": allowed_mentions,
            "components": [
                components.to_dict() for components in (self.components or [])
            ]
        }

        return {
            "type": self.type or CallbackType.MESSAGE,
            "data": {k: i for k, i in resp.items() if i}
        }

    def serialize(self) -> Tuple[str, Union[Payload, Dict]]:
        """
        Creates the data that the discord API wants for the message object

        :return: (content_type, data)
        """

        if not self.attachments:
            return "application/json", self.to_dict()

        form = FormData()
        form.add_field("payload_json", json.dumps(self.to_dict()))
        form.add_fields(
            *(
                (file.filename, file.content)
                for file in self.attachments
            )
        )

        # for file in self.attachments:
        #     form.add_field("file", file.content, filename=file.filename)

        payload = form()
        return payload.headers["Content-Type"], payload
