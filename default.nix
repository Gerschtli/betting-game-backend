with import <nixpkgs> { };

python36Packages.buildPythonPackage rec {
  pname = "betting-game-backend";
  version = "0.1.0";

  src = ./.;

  propagatedBuildInputs = with python36Packages; [
    flask
  ];
}
