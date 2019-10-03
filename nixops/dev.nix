let
  app = import ./app.nix;
  appDir = "/var/www/${app.name}";
in

{
  network.description = app.description;

  bgb =
    { config, lib, pkgs, ... }:
    lib.mkMerge [
      {
        deployment = {
          targetEnv = "virtualbox";

          virtualbox = {
            memorySize = 1024;
            headless = true;

            sharedFolders.${app.name} = {
              hostPath = toString ../.;
              readOnly = false;
            };
          };
        };

        fileSystems.${appDir} = {
          device = app.name;
          fsType = "vboxsf";
          options = [ "uid=${toString app.uid}" "gid=${toString app.uid}" ];
        };

        virtualisation.virtualbox.guest.enable = true;
      }

      {
        networking.firewall.allowedTCPPorts = [ config.services.mysql.port ];

        services.mysql = {
          # Need to run:
          # CREATE DATABASE betting_game;
          # CREATE USER 'betting_game'@'%' IDENTIFIED BY 'testpw';
          # GRANT ALL PRIVILEGES ON betting_game.* TO 'betting_game'@'%';
          # CREATE USER 'betting_game'@'localhost' IDENTIFIED BY 'testpw';
          # GRANT ALL PRIVILEGES ON betting_game.* TO 'betting_game'@'localhost';
          enable = true;
          package = pkgs.mariadb;
        };

        systemd.services.flask-server = {
          description = "Flask Development Server";
          after = [ "network.target" ];
          wantedBy = [ "multi-user.target" ];
          environment = {
            APP_CONFIG_FILE = appDir + "/app/config/dev.py";
            FLASK_APP = appDir + "/app:create_app()";
            FLASK_ENV = "development";
          };
          serviceConfig =
            let python = pkgs.python36.withPackages app.libraries; in
            {
              ExecStartPre = ''
                ${python}/bin/python -m flask db upgrade --directory=${appDir}/migrations
              '';
              ExecStart = ''
                ${python}/bin/python -m flask run --host=0.0.0.0 --port=${toString app.port}
              '';
              User = app.user;
              Restart = "always";
            };
        };
      }

      app.config
    ];
}
