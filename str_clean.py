#    EcoleDirecte Bot (str_clean.py)
#    Copyright (C) 2023 MrBeam89_
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

import re
import html

def clean(input_string):
    # Convert HTML entities to corresponding characters
    input_string = html.unescape(input_string)
    
    # Remove HTML tags
    clean = re.compile('<.*?>')
    return re.sub(clean, '', input_string).rstrip('\n')
