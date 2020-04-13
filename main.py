import argparse
from orchestrator import Orchestrator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="url of containing file paths", type=str)
    parser.add_argument("--file_type", help="file type to be downloaded", type=str)
    parser.add_argument("--download_to", help="path of the location where you want to download the files", type=str)
    parser.add_argument("--start_tag", help="start tag, row starts here", type=str)
    parser.add_argument("--end_tag", help="end tag, row ends here", type=str)

    args = parser.parse_args()

    orch = Orchestrator(args.url, args.file_type, args.download_to)
    orch.orchestrate(args.start_tag, args.end_tag)


if __name__ == "__main__":
    main()
