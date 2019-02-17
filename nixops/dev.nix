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
        nixpkgs.overlays = [
          # fix reloading bug in flask development server
          # see https://github.com/NixOS/nixpkgs/issues/42924#issuecomment-409101368
          (self: super: {
            python36Packages = (super.python36Packages or {}) // {
              werkzeug = super.python36Packages.werkzeug.overrideAttrs (oldAttrs: rec {
                postPatch = ''
                  substituteInPlace werkzeug/_reloader.py \
                    --replace "rv = [sys.executable]" "return sys.argv"
                '';
                doCheck = false;
              });
            };
          })
        ];

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
            FLASK_ENV = "development";
          };
          serviceConfig = {
            ExecStart =
              let
                python = pkgs.python36.withPackages (ps: app.libraries ps);
              in
                "${python}/bin/python -m flask run --host=0.0.0.0 --port=${toString app.port}";
            User = app.user;
            Restart = "always";
          };
        };
      }

      app.config
    ];
}
