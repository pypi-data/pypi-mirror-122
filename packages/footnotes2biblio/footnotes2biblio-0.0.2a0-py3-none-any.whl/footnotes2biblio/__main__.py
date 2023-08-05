import argparse
from .parsers import FootnoteParser

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("src", help="the path of the source doc you want to pull footnotes from")
	parser.add_argument("dst", help="the path of the destination doc you want the pulled footnotes to go into")
	args = parser.parse_args()

	f2b = FootnoteParser()
	f2b.make_biblio(args.src, args.dst)

if __name__ == "__main__":
	main()