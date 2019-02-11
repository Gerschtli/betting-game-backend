let
  app = import ./app.nix;
  appDir = "/var/www/${app.name}";
in

{
  network.description = app.description;

  node =
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
        networking.firewall = {
          enable = true;
          allowedTCPPorts = [ 5000 ];
          allowPing = true;
        };

        services.mysql = {
          # set password with:
          # SET PASSWORD FOR root@localhost = PASSWORD('password');
          enable = true;
          package = pkgs.mariadb;
        };

        systemd.services.flask-server = {
          description = "Flask Development Server";
          after = [ "network.target" ];
          wantedBy = [ "multi-user.target" ];
          environment = {
            FLASK_APP = appDir + "/app";
            # FLASK_ENV = "development";
          };
          serviceConfig = {
            ExecStart = "${pkgs.python36Packages.flask}/bin/flask run --host=0.0.0.0";
            User = app.user;
            Restart = "always";
          };
        };
      }

      app.config
    ];
}
