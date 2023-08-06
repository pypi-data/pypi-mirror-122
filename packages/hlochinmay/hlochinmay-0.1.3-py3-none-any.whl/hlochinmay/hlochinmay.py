import argparse

def hello(name):
    # return "Hello "+ name
    print("Hello "+ name)

def main():
    parser = argparse.ArgumentParser(description="write your name as an argument")
    parser.add_argument('-name', '--name', default=None,  nargs='?', type=str, help='A name for the computer to greet')

    args = parser.parse_args()
    name = args.name
    if name == 'None' or name == None: name = "Stranger"
    
    hello(name)

if __name__ == "__main__":
    main()
