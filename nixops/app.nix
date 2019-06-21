rec {
  name = "betting-game-backend";
  description = "Betting Game Backend";
  user = "worker";
  uid = 1100;
  port = 5000;

  config = {
    networking.firewall = {
      enable = true;
      allowedTCPPorts = [ port ];
      allowPing = true;
    };

    time.timeZone = "Europe/Berlin";

    users = {
      groups.${user} = {
        gid = uid;
      };

      users.${user} = {
        inherit uid;
        group = user;
        isSystemUser = true;
        useDefaultShell = true;
      };
    };
  };

  flask-jwt-extended = ps: ps.buildPythonPackage rec {
    pname = "Flask-JWT-Extended";
    version = "3.17.0";

    src = ps.fetchPypi {
      inherit pname version;
      sha256 = "1hz7b5l7ww7zmgv8hbji3r92xmh3bn29lnwmpxrm25sbgccnzilp";
    };

    propagatedBuildInputs = with ps; [
      flask pyjwt werkzeug
    ];

    checkInputs = with ps; [ pytest ];
    checkPhase = ''
      pytest tests/
    '';
  };

  flask_migrate = ps: ps.flask_migrate.overridePythonAttrs (old: rec {
    version = "2.5.2";
    src = ps.fetchPypi {
      inherit (old) pname;
      inherit version;
      sha256 = "00nm76w4xymsiih6hq8y46wp026v7zkzq15cx39hp929ba3z2vx9";
    };
    checkInputs = old.checkInputs ++ [ ps.flask_script ];
    propagatedBuildInputs = with ps; [ flask flask_sqlalchemy alembic ];
  });

  pyrsistent = ps: ps.pyrsistent.overridePythonAttrs (old: rec {
    pname = "pyrsistent";
    version = "0.14.11";
    src = ps.fetchPypi {
      inherit pname version;
      sha256 = "1qkh74bm296mp5g3r11lgsksr6bh4w1bf8pji4nmxdlfj542ga1w";
    };
  });

  perf = ps: ps.buildPythonPackage rec {
    pname = "perf";
    version = "1.6.0";

    src = ps.fetchPypi {
      inherit pname version;
      sha256 = "1vrv83v8rhyl51yaxlqzw567vz5a9qwkymk3vqvcl5sa2yd3mzgp";
    };

    propagatedBuildInputs = with ps; [ six ];

    doCheck = false;
    checkInputs = with ps; [ nose2 psutil ];
    checkPhase = "nosetests";
  };

  jsonschema = ps: ps.jsonschema.overridePythonAttrs (old: rec {
    version = "3.0.1";
    src = ps.fetchPypi {
      inherit (old) pname;
      inherit version;
      sha256 = "03g20i1xfg4qdlk4475pl4pp7y0h37g1fbgs5qhy678q9xb822hc";
    };
    doCheck = false;
    checkInputs = (
      if old ? buildInputs
      then old.buildInputs
      else old.checkInputs
    ) ++ [
      ps.twisted
      (perf ps)
    ];
    propagatedBuildInputs = old.propagatedBuildInputs ++ [
      ps.attrs
      ps.setuptools_scm
      ps.six
      (pyrsistent ps)
    ];
  });

  libraries = ps: [
    ps.flask
    ps.flask_sqlalchemy
    ps.flask-cors
    ps.flask-restful
    ps.mysqlclient
    ps.passlib
    ps.wrapt
    (flask-jwt-extended ps)
    (flask_migrate ps)
    (jsonschema ps)
  ];

  devLibraries = ps: [
    ps.freezegun
    ps.pytest
    ps.pytestrunner
  ];
}
