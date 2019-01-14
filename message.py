import json
import struct


class MessageHandler(object):
    def __init__(self):
        self._message_buffer = ""
        self._header_len = None
        self._header = None
        self._content = None

    @staticmethod
    def pack_message(content):
        content_bytes = MessageHandler.json_encode(content)

        header = {"content_length": len(content_bytes)}
        header_bytes = MessageHandler.json_encode(header)

        fixed_header = struct.pack(">H", len(header_bytes))

        message = fixed_header + header_bytes + content_bytes
        return message

    @staticmethod
    def json_encode(content):
        return json.dumps(content, ensure_ascii=False).encode("utf-8")

    @staticmethod
    def json_decode(content):
        return json.loads(content)
        #return json.loads(content, encoding="uft-8")

    def unpack_message(self, message_buffer):
        self._message_buffer += message_buffer

        if not self._header_len:
            self._unpack_fixed_header()
        if not self._header:
            self._unpack_header()
        if not self._content:
            self._unpack_content()
        else:
            content = self._content
            self._header_len = None
            self._header = None
            self._content = None
            return content
        return None

    def _unpack_fixed_header(self):
        length = 2
        if len(self._message_buffer) >= length:
            self._header_len = struct.unpack(">H", self._message_buffer[:length])[0]
            self._message_buffer = self._message_buffer[length:]

    def _unpack_header(self):
        if len(self._message_buffer) >= self._header_len:
            header_bytes = self._message_buffer[:self._header_len]
            self._header = MessageHandler.json_decode(header_bytes)
            self._message_buffer = self._message_buffer[self._header_len:]

    def _unpack_content(self):
        content_lenght = self._header.get("content_length")
        if len(self._message_buffer) >= content_lenght:
            content_bytes = self._message_buffer[:content_lenght]
            self._content = MessageHandler.json_decode(content_bytes)
            self._message_buffer = self._message_buffer[content_lenght:]

    @property
    def message_buffer(self):
        return self._message_buffer

