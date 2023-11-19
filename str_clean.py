import re
import html

def clean(input_string):
    # Convert HTML entities to corresponding characters
    input_string = html.unescape(input_string)
    
    # Remove HTML tags
    clean = re.compile('<.*?>')
    return re.sub(clean, '', input_string).rstrip('\n')
