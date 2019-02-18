{ pkgs ? import <nixpkgs> { } }:

pkgs.python36Packages.buildPythonApplication rec {
  pname = "betting-game-backend";
  version = "0.1.0";

  src = ./.;

  doCheck = false;

  propagatedBuildInputs = (import ./nixops/app.nix).libraries pkgs.python36Packages;
}
