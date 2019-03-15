#!/usr/bin/env bash

here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

export nixpkgs_snapshot=$(eval echo "$(nix-instantiate --eval -E "(import \"$here/nixpkgs-version.nix\").url")")
