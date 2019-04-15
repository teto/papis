with import <nixpkgs> {};

let
  nvimConfig = {
      # extraPython3Packages = ps: with ps; ([ python-slugify bibtexparser filetype]);
  };

  my_nvim = genNeovim [ papis ] nvimConfig;

  prog = papis.overrideAttrs (oa: {
      # buildInputs = (oa.buildInputs or []) ++ [ my_nvim  ];
      src = ./.;

      postShellHook = ''
        export SOURCE_DATE_EPOCH=315532800
        export PATH="${my_nvim}/bin:$PATH"
        echo "importing a custom nvim ${my_nvim}"
        source scripts/shell_completion/build/bash/papis
      '';
    });

in
  prog



