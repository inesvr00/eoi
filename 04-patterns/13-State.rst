El patrón State (Estado)
------------------------

Propósito
^^^^^^^^^

Permite que un objeto modifique su comportamiento cada vez que cambie su
estado interno. Parecerá que cambia la clase del objeto.

También conocido como
^^^^^^^^^^^^^^^^^^^^^

Objects for States (Estados como Objetos)

Motivación
^^^^^^^^^^

Pensemos en una clase ``Conexion`` que representa una conexión entre dos
ordenadores. Un objeto ``Conexion`` puede encontrarse en uno de los
siguientes tres estados:

-  Establecida
-  Escuchando
-  Cerrada

Cuando un objeto ``Conexion`` recibe peticiones de otros objetos, les
responde de distinta forma dependiendo de su estado actual. Por ejemplo,
el efecto de una petición ``open`` depende de si la conexión se
encuentra en su estado ``Cerrada`` o en su estado ``Establecida``.

El patrón State describe cómo puede ``Conexion`` exhibir un
comportamiento diferente en cada estado.

La idea clave de este patrón es introducir una clase abstracta llamada
``EstadoConn`` que representa los estados de la conexión de red.

La clase ``EstadoConn`` declara una interfaz común para todas las clases
que representarán cada uno de los diferentes estados. Las subclases
implementan el comportamiento específico de cada estado.

Por ejemplo, las clases ``EstadoEstablecida`` y ``EstadoCerrada``
implementan el comportamiento concreto de los estados ``Establecida`` y
``Cerrada`` respectivamente.

La clase ``Conexion`` mantiene un atributo de estado, que es una
instancia de una subclase de ``EstadoConn``. Esto representa el estado
actual de la conexión. La clase ``Conexion`` delega todas las peticiones
relativas al estado a este componente.

El siguiente fragmento de codigo implementa el controlador de un
personaje de un juego de plataformas. Queremos que al pulsar la tecla
``B``, el personaje salta::

    class Hero:
        ...
        def handle_input(self, key_press):
            if key_press == 'B':
                self.velocity.y += JUMP_VELOCITY
                self.set_graphic(Image(HERO_JUMP))

Funciona, pero tiene un fallo. ¿Puedes descubrir cual es?

.. figure:: img/superman.gif
   :alt: Superman!

   Superman!

Nuestro heroe puede volar! Si pulsa el boton de volar otra vez cuando el
personaje esta en el aire, vuelve a impulsarse para arriba. No es
exactemente lo que buscabamos.

Pero podemos resolverlo facilmente con un flag booleano::

    class Hero:
        ...
        def handle_input(self, key_press):
            if key_press == 'B' and not self.is_jumping:
                self.velocity.y += JUMP_VELOCITY
                self.graphic = Image(HERO_JUMP)
                self.is_jumping = True

Ahora queremos que se pueda agachar con la tecla ``C``, para esquivar un
ataque, facilisimo::

    class Hero:
        ...
        def handle_input(self, key_press):
            if key_press == 'B' and not self.is_jumping:
                self.velocity.y += JUMP_VELOCITY
                self.graphic = Image(HERO_JUMP)
                self.is_jumping = True
            if key_press == 'C':
                self.graphic = Image(HERO_DIVE)

¿Ves el fallo ahora?

Si pulsamos `C` durante un salto, la imagen cambia a la de agachado.

Hay que arreglarlo con otro ``if``::

    class Hero:
        ...
        
        def handle_input(self, key_press):
            if key_press == 'B' and not self.is_jumping:
                self.velocity.y += JUMP_VELOCITY
                self.graphic = Image(HERO_JUMP)
                self.is_jumping = True
            if key_press == 'C':
                if not self.is_jumping:
                    self.graphic = Image(HERO_DIVE)

Ahora queremos que el personaje no pueda saltar si esta agachado. ¿Qué
necesitas y como lo implementarias.

Una forma podría ser::

    class Hero:
        ...
        
        def handle_input(self, key_press):
            if key_press == 'B' and not self.is_jumping and not self.is_diving:
                self.velocity.y += JUMP_VELOCITY
                self.set_graphic(HERO_JUMP)
                self.is_jumping = True
            if key_press == 'C' and not self.is_jumping:
                self.set_graphic(HERO_DIVE)
                self.is_diving = True

Ya tenemos un código feo, con un monton de if y ni siquiera hemos
empezado con cosas como atacar o simplemente moverse. 

El problema es que tenemos muchos estados diferentes, y controlarlos a
base de variables booleanas se vuelve muy pronto muy complicado.

Vamos a solucionarlo usando el patron estado. Vamos a crear tres estados
(los que tenemos por ahora): Sn hacer nada (*idle*), saltando
(*jumping*) y agachado (*diving*):

En otros lenguajes usaremos una clase base `StateBase`. No es
estrictamnte necesaria, porque tenemos *Dock-Typing* con Python, pero en
este caso me interesa tener una clase base que defina los verbos y que
por defecto no haga nada, y el constructor tambien me vale para todas
las clases derivadas::

    class StateBase:

        def __init__(self, hero):
            self.hero = hero
    
        def jump(self):
            pass
    
        def dive(self):
            pass

Definimos el estado *idle*. En este estado podemos saltar o
agacharnos::

    class StateIdle(StateBase):
    
        def jump(self):
            self.hero.velocity.y += JUMP_VELOCITY
            self.hero.set_graphic(HERO_JUMP)
    
        def dive(self):
            self.set_graphic(HERO_DIVE)

Ahora la clase para el estado “Saltando”. Aqui no podemos ni saltar otra
vez ni agacharnos, asi que con los comportamientos por defecto nos
vale::

    class StateJumping(StateBase):
        pass

Y lo mismo para el estado agachado::

    class StateJumping(StateBase):
        pass

Ahora nuestro heroe necesita un atributo para almacenar el objeto
estado::

    class Hero:

    def __init__(self):
        self.state = IdleState(self)
        
    def handle_input(self, key_press):
        if key_press == 'B':
            self.state.jump()
        elif key_press == 'C' and not self.is_jumping:
            self.state.dive()
