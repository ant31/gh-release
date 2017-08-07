#!/usr/bin/env python

import argparse
import mimetypes
import os
import requests


class UploadGH(object):
    def __init__(self, repo, token=None):
        self.token = os.getenv("GITHUB_TOKEN", token)
        self.endpoint = "https://api.github.com/repos/%s" % repo

    def headers(self, extra={}):
        headers = {'Authorization': "token %s" % self.token}
        headers.update(extra)
        return headers

    def get_release(self, tag):
        path = self.endpoint + "/releases/tags/%s" % tag
        resp = requests.get(path)
        resp.raise_for_status()
        return resp.json()

    def get_existing_asset(self, name, release_id):
        path = self.endpoint + "/releases/%s/assets" % release_id
        resp = requests.get(path)
        assets = resp.json()

        if resp.status_code < 299:
            for asset in assets:
                if asset['name'] == name:
                    return asset

        return None

    def delete_asset(self, asset):
        resp = requests.delete(asset['url'], headers=self.headers())
        resp.raise_for_status()

    def upload(self, filepath, tag, name=None,
               overwrite=True, contenttype="application/octet-stream"):
        release = self.get_release(tag)
        upload_url = release['upload_url'].split("{")[0]
        name = name or os.path.basename(filepath)
        data = open(filepath, "rb").read()

        if overwrite:
            previous_asset = self.get_existing_asset(name, release['id'])
            if previous_asset:
                self.delete_asset(previous_asset)

        if contenttype is None:
            mimetypes.init()
            contenttype = mimetypes.guess_type(filepath)[0]

        resp = requests.post(upload_url, data=data,
                             headers=self.headers({'Content-Type': contenttype}),
                             params={"name": name})

        return resp


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


if __name__ == "__main__":
    cli()
