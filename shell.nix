with import <nixpkgs> { };

(import ./. { }).overrideDerivation (old: {
  name = old.pname;

  buildInputs = old.buildInputs
    ++ (with python36Packages; [
      flake8
      git-crypt
      isort
      mypy
      pylint
      python-language-server
    ]);

  APP_CONFIG_FILE = toString app/config/cli.py;
  PYTHONDONTWRITEBYTECODE = 1;
})
