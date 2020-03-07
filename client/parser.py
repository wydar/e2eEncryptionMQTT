import argparse

def parse_command():
    parser = argparse.ArgumentParser(description="IoT Device MQQT Client simulator")

    parser.add_argument('-i', '--input', action='store_true', help="Input device exists")
    parser.add_argument('-o', '--output', action='store_true', help="Output device exists")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable Verbose Mode")
    parser.add_argument('-n', '--nauth', type=int, default=6,help="Lenght of authentication code (Default:6)")
    
    return parser.parse_args()