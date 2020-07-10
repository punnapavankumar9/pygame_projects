import cx_Freeze

executables = [cx_Freeze.Executable('snakegame.py')]

cx_Freeze.setup(
    name='Snake Game',
    options={
        'build_exe':{
            'packages': ['pygame'],
            'includes': []
        }
    },
    executables=executables
)