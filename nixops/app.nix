rec {
  name = "betting-game-backend";
  description = "Betting Game Backend";
  user = "worker";
  uid = 1100;

  config =
    {
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
}
