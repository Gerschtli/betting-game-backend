with import ./nixops/nixpkgs.nix;

let
  app = import ./nixops/app.nix;
in

python36Packages.buildPythonApplication rec {
  pname = "betting-game-backend";
  version = "0.1.0";

  src = ./.;

  propagatedBuildInputs = app.libraries python36Packages;
  checkInputs = app.devLibraries python36Packages;

  preCheck = "export APP_CONFIG_FILE=${./app/config/dev.py}";
  postCheck = "export APP_CONFIG_FILE=";
}
