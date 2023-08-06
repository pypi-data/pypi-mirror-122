import argparse
import giftsnippet


def main():
    parser = argparse.ArgumentParser(description="Replace gift-snippets in your gift file with highlighted code images")
    parser.add_argument('file', help='Provide a gift file to replace gift-snippets with highlighted code images')
    args = parser.parse_args()

    try:
        giftsnippet.process_gift_file(args.file)
    except Exception as e:
        print("An error occured: " + getattr(e, 'message', repr(e)))


