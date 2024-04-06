#    EcoleDirecte Bot (str_clean.py)
#    Copyright (C) 2023-2024 MrBeam89_
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <https://www.gnu.org/licenses/>.

import re
import html

def clean(input_string):
    # Convertir les entités HTML en caractères correspondants
    input_string = html.unescape(input_string)
    
    # Enlève les élements HTML
    clean = re.compile('<.*?>')
    return re.sub(clean, '', input_string).rstrip('\n')
