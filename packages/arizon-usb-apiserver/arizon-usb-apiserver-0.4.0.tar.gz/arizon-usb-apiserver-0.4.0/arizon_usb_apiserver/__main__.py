import argparse
import sys

import arizon_usb_apiserver.apiserver as apiserver
import arizon_usb_apiserver.cmd as cmd

parser = argparse.ArgumentParser()

args = sys.argv[1:]
if len(args) == 0:
    exit(print("No arguments provided"))
if args[0] == "configure":
    exit(cmd.configure(args[1:]))
elif args[0] == "apiserver":
    exit(apiserver.serve(args[1:]))
elif args[0] == "apiserver.restful":
    exit(apiserver.serve_restful(args[1:]))
elif args[0] == "apiserver.grpc":
    exit(apiserver.serve_grpc(args[1:]))
elif args[0] == "test.restful":
    exit(cmd.test_restful())
elif args[0] == "test.grpc":
    exit(cmd.test_grpc())
else:
    print("Unknown command: {}".format(args[0]))
