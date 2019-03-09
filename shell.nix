with import <nixpkgs> { };

(import ./. { }).overrideDerivation (old: {
  name = old.pname;

  buildInputs = old.buildInputs
    ++ (with python36Packages; [
      coverage
      flake8
      git-crypt
      isort
      mypy
      python-language-server
    ]);

  APP_CONFIG_FILE = toString app/config/cli.py;
  PYTHONDONTWRITEBYTECODE = 1;
})
