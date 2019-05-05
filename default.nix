with import ./nixops/nixpkgs.nix;

python36Packages.buildPythonApplication rec {
  pname = "betting-game-backend";
  version = "0.1.0";

  src = ./.;

  propagatedBuildInputs = (import ./nixops/app.nix).libraries python36Packages;

  checkInputs = with python36Packages; [
    pytest pytestrunner freezegun
  ];
  preCheck = "export APP_CONFIG_FILE=${./app/config/dev.py}";
  postCheck = "export APP_CONFIG_FILE=";
}
