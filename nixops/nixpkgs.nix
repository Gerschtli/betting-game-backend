import ((import <nixpkgs> { }).fetchzip (import ./nixpkgs-version.nix)) {
  config = { };
  overlays = [
    (self: super:
      {
        python36Packages = (super.python36Packages or {}) // {
          flake8-quotes = super.python36Packages.buildPythonPackage rec {
            pname = "flake8-quotes";
            version = "2.1.0";

            src = super.python36Packages.fetchPypi {
              inherit pname version;
              sha256 = "1v9l9454lxi1zyf1dwp9gkvvkr52dlyr91zv8s1z4wvqi1lgdfjx";
            };

            doCheck = false;
            propagatedBuildInputs = [ self.python36Packages.flake8 ];
          };

          mypy = super.python36Packages.mypy.overridePythonAttrs (old: rec {
            version = "0.730";

            src = super.python36Packages.fetchPypi {
              inherit (old) pname;
              inherit version;
              sha256 = "0ygqviby0i4i3k2mlnr08f07dxvkh5ncl17m14bg4w07x128k9s2";
            };

            propagatedBuildInputs = with self.python36Packages; [
              typed-ast
              psutil
              mypy_extensions
              typing-extensions
            ];
          });

          typed-ast = super.python36Packages.typed-ast.overridePythonAttrs (old: rec {
            version = "1.4.0";

            src = super.fetchFromGitHub {
              owner = "python";
              repo = "typed_ast";
              rev = version;
              sha256 = "0l0hz809f7i356kmqkvfsaswiidb98j9hs9rrjnfawzqcbffzgyb";
            };
          });

          typing-extensions = super.python36Packages.typing-extensions.overridePythonAttrs (old: rec {
            version = "3.7.4";

            src = super.python36Packages.fetchPypi {
              inherit (old) pname;
              inherit version;
              sha256 = "15bx773a5zkk4hkwjl8nb5f8y5741vyyqb9q3jac6kxm1frk5mif";
            };
          });
        };
      }
    )
  ];
}
