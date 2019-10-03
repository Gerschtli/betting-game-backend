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

  libraries = ps: with ps; [
    flask
    flask_mail
    flask_migrate
    flask_sqlalchemy
    flask-cors
    flask-jwt-extended
    flask-restful
    jsonschema
    mysqlclient
    passlib
    wrapt
  ];

  devLibraries = ps: with ps; [
    freezegun
    pytest
    pytestrunner
  ];
}
