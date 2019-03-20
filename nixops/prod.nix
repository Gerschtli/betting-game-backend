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
            package = import ../.;
            python = pkgs.python36.withPackages (ps:
              [ package ps.gunicorn ] ++ app.libraries ps
            );
          in
            {
              description = "Flask Server";
              after = [ "network.target" ];
              wantedBy = [ "multi-user.target" ];
              environment = {
                APP_CONFIG_FILE = "${package}/${python.sitePackages}/app/config/prod.py";
                FLASK_APP = "${package}/${python.sitePackages}/app:create_app()";
              };
              serviceConfig = {
                ExecStartPre = ''
                  ${python}/bin/python -m flask db upgrade \
                    --directory=${package}/migrations
                '';
                ExecStart = ''
                  ${python}/bin/python -m gunicorn.app.wsgiapp \
                    --bind 0.0.0.0:${toString app.port} --workers 4 \
                    --chdir ${package}/${python.sitePackages} app:create_app()
                '';
                User = app.user;
                Restart = "always";
              };
            };
      }

      app.config
    ];
}
