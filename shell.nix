with import ./nixops/nixpkgs.nix;

let
  mypy_extensions_ = python36Packages.buildPythonPackage rec {
    pname = "mypy_extensions";
    version = "0.4.1";

    # Tests not included in pip package.
    doCheck = false;

    src = python36Packages.fetchPypi {
      inherit pname version;
      sha256 = "04h8brrbbx151dfa2cvvlnxgmb5wa00mhd2z7nd20s8kyibfkq1p";
    };

    propagatedBuildInputs = [ python36Packages.typing ];
  };

  typed-ast_ = python36Packages.typed-ast.overridePythonAttrs (old: rec {
    version = "1.3.1";

    src = python36Packages.fetchPypi {
      inherit (old) pname;
      inherit version;
      sha256 = "095l1jfxk1k2z5sijbirg2s5a01r4ig3715zqa075xzf0zx8lvb0";
    };
  });

  mypy_ = python36Packages.mypy.overridePythonAttrs (old: rec {
    version = "0.670";

    src = python36Packages.fetchPypi {
      inherit (old) pname;
      inherit version;
      sha256 = "e80fd6af34614a0e898a57f14296d0dacb584648f0339c2e000ddbf0f4cc2f8d";
    };

    propagatedBuildInputs = [
      python36Packages.lxml
      python36Packages.psutil
      mypy_extensions_
      typed-ast_
    ];
  });

  flake8-quotes = python36Packages.buildPythonPackage rec {
    pname = "flake8-quotes";
    version = "1.0.0";

    src = python36Packages.fetchPypi {
      inherit pname version;
      sha256 = "09ib440hrf5bbsmdbqzbcpkkqqnqdwkaawbqz93bbwxwifnjg4gx";
    };

    propagatedBuildInputs = [ python36Packages.flake8 ];
  };
in

(import ./.).overrideDerivation (old: {
  name = old.pname;

  buildInputs = old.buildInputs
    ++ (with python36Packages; [
      coverage
      flake8
      flake8-quotes
      git-crypt
      isort
      mypy_
      python-language-server
    ]);

  APP_CONFIG_FILE = toString app/config/cli.py;
  PYTHONDONTWRITEBYTECODE = 1;
})
