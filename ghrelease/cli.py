import argparse

from ghrelease.upload_gh import UploadGH


def cli():
    parser = argparse.ArgumentParser()

    parser.add_argument("--api-key", default=None, help="Github API-key")
    parser.add_argument("--repo", required=True, help="Github repo name")
    parser.add_argument("--file", required=True, help="filepath to upload")
    parser.add_argument("--tag", required=True, help="Release tag")
    parser.add_argument("--file-name", help="filename", default=None)
    parser.add_argument("--content-type", help="MimeType", default="application/octet-stream")
    parser.add_argument("--no-overwrite", help="Fail if a previous asset already exists", default=True, action="store_false")

    args = parser.parse_args()

    uploader = UploadGH(args.repo, token=args.api_key)
    resp = uploader.upload(filepath=args.file, tag=args.tag, name=args.file_name,
                           overwrite=args.no_overwrite, contenttype=args.content_type)
    print(resp.status_code)
