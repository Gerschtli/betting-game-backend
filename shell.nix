with import ./nixops/nixpkgs.nix;

let
  app = import ./nixops/app.nix;
in

mkShell {
  buildInputs = app.libraries python36Packages
    ++ app.devLibraries python36Packages
    ++ (with python36Packages; [
      coverage
      flake8
      flake8-quotes
      git-crypt
      isort
      mypy
      python-language-server
    ]);

  APP_CONFIG_FILE = toString app/config/cli.py;
  PYTHONDONTWRITEBYTECODE = 1;
}
