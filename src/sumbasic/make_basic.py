#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#pylint:disable=W0301
#
#  Copyright 2018- William Martinez Bas <metfar@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
"""Prepare a portable Sum BASIC project without depending on sumbuild.""";
import argparse;
import json;
from pathlib import Path;

def main(argv=None):
    parser=argparse.ArgumentParser(prog="makeBasic");
    parser.add_argument("source", help="BASIC file");
    parser.add_argument("--output", help="project directory (defaults to source's parent)");
    parser.add_argument("--name");
    parser.add_argument("--force", action="store_true");
    args=parser.parse_args(argv);
    source=Path(args.source).resolve();
    if not source.is_file() or source.suffix.lower() != ".bas":
        parser.error("source must be an existing .bas file");
    target=Path(args.output).resolve() if args.output else source.parent;
    target.mkdir(parents=True, exist_ok=True);
    if source.parent != target:
        import shutil;
        shutil.copy2(source,target/source.name);
    project_file=target / "project.sum";
    if project_file.exists() and not args.force:
        parser.error("project.sum already exists: use --force to overwrite");
    project={
        "sum_project":1,
        "name":args.name or source.stem,
        "version":"0.1.0",
        "language":"sumbasic",
        "entrypoint":source.name,
        "sources":[source.name],
        "resources":[],
        "dependencies":["sumbasic", "sumcore"],
        "interface":{"backend":"auto","screen":"auto"},
        "build":{"targets":["linux"],"console":True,
                 "host":{"backend":"nuitka","bundle":"auto","layout":"onefile"},
                 "exclude_dev":True},
    };
    project_file.write_text(json.dumps(project,indent=2,ensure_ascii=False)+"\n",encoding="utf-8");
    print(project_file);
    return 0;

if __name__ == "__main__":
    raise SystemExit(main());
