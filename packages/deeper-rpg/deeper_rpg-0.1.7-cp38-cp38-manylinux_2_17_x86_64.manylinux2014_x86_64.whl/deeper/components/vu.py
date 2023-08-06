import glm

from .. import Component

class Vu(Component):
    position: glm.vec3 = glm.vec3()
    def __init__(self) -> None:
        super().__init__()