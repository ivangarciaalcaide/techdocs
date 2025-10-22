# docs/main.py

def define_env(env):
    """
    Define una variable simple para la prueba.
    """
    # Esta variable se inyectará como {{ autor_nombre }}
    env.variables['autor_nombre'] = "Tecnicaso"