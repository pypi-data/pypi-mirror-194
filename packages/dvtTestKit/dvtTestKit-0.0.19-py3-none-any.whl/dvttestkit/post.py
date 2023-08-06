import sys
from testKitUtils import post

if __name__ == "__main__":
    # check if there are enough arguments
    if len(sys.argv) < 3:
        print("Usage: python my_script.py topic payload [retain]. Default retain is True")
        sys.exit(1)

    # parse arguments
    topic = sys.argv[1]
    payload = sys.argv[2]
    if len(sys.argv) > 3:
        retain = sys.argv[3].lower() == "false"
    else:
        retain = True

    # call post function
    post(topic, payload, retain)
