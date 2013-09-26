import sys
from engine import handle_text, get_text

handle_text(sys.argv[1], sys.argv[2])
for text in get_text(sys.argv[1]):
    print text
