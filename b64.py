#    EcoleDirecte Bot (b64.py)
#    Copyright (C) 2023-2024 MrBeam89_
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import base64
def decode_base64(b64_string:str)->str:
    bytes = b64_string.encode("utf-8")
    converted_bytes = base64.b64decode(bytes)
    decoded_str = converted_bytes.decode("utf-8")
    return decoded_str
