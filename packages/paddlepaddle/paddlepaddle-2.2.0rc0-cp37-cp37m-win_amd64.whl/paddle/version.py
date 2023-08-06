# THIS FILE IS GENERATED FROM PADDLEPADDLE SETUP.PY
#
full_version    = '2.2.0-rc0'
major           = '2'
minor           = '2'
patch           = '0-rc0'
rc              = '0'
istaged         = True
commit          = 'c576169b8c4b18d4a714133e459c0380dacf84b9'
with_mkl        = 'ON'

def show():
    if istaged:
        print('full_version:', full_version)
        print('major:', major)
        print('minor:', minor)
        print('patch:', patch)
        print('rc:', rc)
    else:
        print('commit:', commit)

def mkl():
    return with_mkl
