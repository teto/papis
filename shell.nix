# { pkgs ? with import <nixpkgs> {} }:
with import <nixpkgs> {};
let
  # Python
  # papis = with python3Packages; toPythonApplication papis;
  prog = papis.overrideAttrs(oa: {
    # echo "SOURCE_DATE_EPOCH: $SOURCE_DATE_EPOCH"
    # export SOURCE_DATE_EPOCH=315532800
    # mkdir -p "$tmp_path/@pythonSitePackages@"
    # python -m pip install -e . --prefix $tmp_path >&2
    postShellHook = ''
      export PYTHONPATH="$tmp_path/lib/python3.7/site-packages:$PYTHONPATH"
      python -m pip install -e . --prefix $tmp_path >&2

    '';
  });
in
  prog

