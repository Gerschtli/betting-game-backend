{ pkgs ? import <nixpkgs> { } }:

pkgs.python36Packages.buildPythonPackage rec {
  pname = "betting-game-backend";
  version = "0.1.0";

  src = ./.;

  propagatedBuildInputs = (import ./nixops/app.nix).libraries pkgs.python36Packages;
}
