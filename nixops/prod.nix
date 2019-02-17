let
  app = import ./app.nix;
in

{
  network.description = app.description;

  bgb =
    { config, lib, pkgs, ... }:
    lib.mkMerge [
      {
        deployment = {
          targetEnv = "container";
          container.host = "app.betting-game";
        };
      }

      {
        systemd.services.flask-server =
          let
            package = import ../. { inherit pkgs; };
            python = pkgs.python36.withPackages (ps:
              [ package ps.gunicorn ] ++ app.libraries ps
            );
          in
            {
              description = "Flask Server";
              after = [ "network.target" ];
              wantedBy = [ "multi-user.target" ];
              environment = {
                APP_CONFIG_FILE = package + "/config/prod.py";
              };
              serviceConfig = {
                ExecStart = ''
                  ${python}/bin/python -m gunicorn.app.wsgiapp \
                    --bind '0.0.0.0:${toString app.port}' --workers 4 \
                    app:app
                '';
                User = app.user;
                Restart = "always";
              };
            };
      }

      app.config
    ];
}
