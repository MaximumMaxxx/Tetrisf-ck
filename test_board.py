from cgi import test
from interperter import *


def test_helloWorld():
    # Test if the interperter can run a simple hello world program
    sample = "oggggggggyrgggggggggobcrpoggggyrgggggggobcrgpgggggggppgggpooggggggyrgggggggobcrggpbbbbbbbbbbbbpoggggggyrgggggggggobcrgprpgggpbbbbbbpbbbbbbbbpoooggggyrggggggggobcrgp"

    # Convert the sample to a list of single characters
    sample = list(sample)
    assert interpreter(sample) == "Hello, World!"
