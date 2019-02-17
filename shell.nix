with import <nixpkgs> { };

(import ./. { }).overrideDerivation (old: {
  name = old.pname;

  buildInputs = old.buildInputs
    ++ (with python36Packages; [
      git-crypt
      python-language-server
    ]);

  PYTHONDONTWRITEBYTECODE = 1;
})
