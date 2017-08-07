import json
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

    def create_release(self, tag):
        path = self.endpoint + "/releases"
        params = {"tag_name": tag,
                  "name": tag,
                  "body": "Release %s" % tag}
        resp = requests.post(path, data=json.dumps(params), headers=self.headers())
        resp.raise_for_status()
        return resp

    def get_release(self, tag):
        path = self.endpoint + "/releases/tags/%s" % tag
        resp = requests.get(path)
        if resp.status_code == 404:
            resp = self.create_release(tag)
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
