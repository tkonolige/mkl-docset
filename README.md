# MKL Docset

A script that generates a docset for MKL

## Usage

1. Copy the contents of `$MKL_ROOT/en/mkl/common/mklman_c/` to `mkl.docset/Contents/Resources/Documents`.
2. Run `python gen_docset.py`.
3. Verify `mkl.docset/Contents/Info.plist` has the correct index file under the key `dashIndexFilePath`.
