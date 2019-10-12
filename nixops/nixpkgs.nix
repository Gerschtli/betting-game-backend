import ((import <nixpkgs> { }).fetchzip (import ./nixpkgs-version.nix)) {
  config = { };
  overlays = [
    (self: super:
      {
        python36 = super.python36.override {
          packageOverrides = self: super: {

            # production packages
            flask_migrate = super.flask_migrate.overridePythonAttrs (old: rec {
              version = "2.5.2";

              src = super.fetchPypi {
                inherit (old) pname;
                inherit version;
                sha256 = "00nm76w4xymsiih6hq8y46wp026v7zkzq15cx39hp929ba3z2vx9";
              };

              checkInputs = old.checkInputs ++ [ self.flask_script ];
              propagatedBuildInputs = with self; [ flask flask_sqlalchemy alembic ];
            });

            jsonschema = super.jsonschema.overridePythonAttrs (old: rec {
              version = "3.0.1";

              src = super.fetchPypi {
                inherit (old) pname;
                inherit version;
                sha256 = "03g20i1xfg4qdlk4475pl4pp7y0h37g1fbgs5qhy678q9xb822hc";
              };

              doCheck = false;

              propagatedBuildInputs = with self; old.propagatedBuildInputs ++ [
                attrs
                pyrsistent
                setuptools_scm
                six
              ];
            });

            perf = super.buildPythonPackage rec {
              pname = "perf";
              version = "1.6.0";

              src = super.fetchPypi {
                inherit pname version;
                sha256 = "1vrv83v8rhyl51yaxlqzw567vz5a9qwkymk3vqvcl5sa2yd3mzgp";
              };

              doCheck = false;

              propagatedBuildInputs = with self; [ six ];
            };

            pyrsistent = super.pyrsistent.overridePythonAttrs (old: rec {
              pname = "pyrsistent";
              version = "0.14.11";

              src = super.fetchPypi {
                inherit pname version;
                sha256 = "1qkh74bm296mp5g3r11lgsksr6bh4w1bf8pji4nmxdlfj542ga1w";
              };
            });

            # development packages
            flake8-quotes = super.buildPythonPackage rec {
              pname = "flake8-quotes";
              version = "2.1.0";

              src = super.fetchPypi {
                inherit pname version;
                sha256 = "1v9l9454lxi1zyf1dwp9gkvvkr52dlyr91zv8s1z4wvqi1lgdfjx";
              };

              doCheck = false;
              propagatedBuildInputs = [ self.flake8 ];
            };

            mypy = super.mypy.overridePythonAttrs (old: rec {
              version = "0.730";

              src = super.fetchPypi {
                inherit (old) pname;
                inherit version;
                sha256 = "0ygqviby0i4i3k2mlnr08f07dxvkh5ncl17m14bg4w07x128k9s2";
              };

              propagatedBuildInputs = with self; [
                typed-ast
                psutil
                mypy_extensions
                typing-extensions
              ];
            });

            typed-ast = super.typed-ast.overridePythonAttrs (old: rec {
              version = "1.4.0";

              src = super.fetchFromGitHub {
                owner = "python";
                repo = "typed_ast";
                rev = version;
                sha256 = "0l0hz809f7i356kmqkvfsaswiidb98j9hs9rrjnfawzqcbffzgyb";
              };
            });

            typing-extensions = super.typing-extensions.overridePythonAttrs (old: rec {
              version = "3.7.4";

              src = super.fetchPypi {
                inherit (old) pname;
                inherit version;
                sha256 = "15bx773a5zkk4hkwjl8nb5f8y5741vyyqb9q3jac6kxm1frk5mif";
              };
            });

            werkzeug = super.werkzeug.overridePythonAttrs (old: rec {
              version = "0.16.0";

              src = super.fetchPypi {
                inherit (old) pname;
                inherit version;
                sha256 = "1rrklk7567pwdmd1694pwad8yd3bdhc74fg2dwj3nwxm8x3r503j";
              };
            });

          };
        };

        python36Packages = self.python36.pkgs;
      }
    )
  ];
}
