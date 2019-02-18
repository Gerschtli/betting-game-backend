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

  libraries = ps: [
    ps.flask
    ps.flask_migrate
    ps.flask_sqlalchemy
    ps.flask-restful
    ps.mysqlclient
    ps.passlib
    (flask-jwt-extended ps)
  ];
}
