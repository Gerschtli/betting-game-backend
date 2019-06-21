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
    version = "0.700";

    src = python36Packages.fetchPypi {
      inherit (old) pname;
      inherit version;
      sha256 = "1zxfi5s9hxrz0hbaj4n513az17l44pxl80r62ipjc0bsmbcic2xi";
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
    version = "2.0.1";

    src = python36Packages.fetchPypi {
      inherit pname version;
      sha256 = "0f10q2580bzxmr0lic42q32qbyf3aq42di91wyl04hrd8xmszj8h";
    };

    doCheck = false;
    propagatedBuildInputs = [ python36Packages.flake8 ];
  };

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
      mypy_
      python-language-server
    ]);

  APP_CONFIG_FILE = toString app/config/cli.py;
  PYTHONDONTWRITEBYTECODE = 1;
}
