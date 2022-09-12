#!/usr/bin/env python3

import os
import sys
import UnityPy

usage = f"""
{sys.argv[0]}: View or extract assets from a Unity asset bundle. Using UnityPy.
Copyright Thomas van der Berg 2022. Licensed under GNU GPLv3.

Usage:
    {sys.argv[0]} <asset-bundle-file>                view files and file types in asset bundle
    {sys.argv[0]} <asset-bundle-file> <full-path>    extract a single file from asset bundle. Only Texture2D supported for now.
"""

def view_asset_bundle(assetbundlefile):
    env = UnityPy.load(assetbundlefile)

    for path,obj in env.container.items():
        print(path, " : ", obj.type.name)

    return 0

def extract_asset(assetbundlefile, path):
    env = UnityPy.load(assetbundlefile)

    for objpath,obj in env.container.items():
        if objpath != path:
            continue
        if obj.type.name in ["Texture2D", "Sprite"]:
            data = obj.read()
            outfilename = data.name + ".png"
            print(f"Extracting {outfilename}...")
            data.image.save(outfilename)
        elif obj.type.name == "TextAsset":
            data = obj.read()
            outfilename = data.name
            if objpath[-5:] == ".json":
                outfilename += ".json" # for .dfmod.json: avoid accidentally overwriting the .dfmod file itself due to name conflict ...
            print(f"Extracting {outfilename}...")
            with open(outfilename, "wb") as f:
                f.write(bytes(data.script))
        else:
            outfilename = objpath.split("/")[-1]
            print(f"Extracting {outfilename}...")
            with open(outfilename, "wb") as f:
                f.write(obj.get_raw_data())
        return 0
    print(f"Error: can't find {path} in {assetbundlefile}", file=sys.stderr)
    return 1

def main():
    if len(sys.argv) == 2:
        return view_asset_bundle(sys.argv[1])
    elif len(sys.argv) == 3:
        return extract_asset(sys.argv[1], sys.argv[2])
    else:
        print(usage)
        return 2

if __name__ == '__main__':
    sys.exit(main())
