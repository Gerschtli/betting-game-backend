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

  libraries = ps: [
    ps.flask
    ps.flask_migrate
    ps.flask_sqlalchemy
    ps.mysqlclient
  ];
}
