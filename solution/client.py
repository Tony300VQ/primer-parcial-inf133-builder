from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
personajes={}
class Personaje():
    def __init__(self):
        self.id=None
        self.name=None
        self.level=None
        self.role=None
        self.charisma=None
        self.strength=None
        self.dexterity=None
    def __str__(self):
        return f"Id: {self.id} Name:{self.name} Level: {self.level} Role: {self.role} Charisma: {self.charisma} Strenght: {self.strength} Dexterity: {self.dexterity}"

class PersonajeBuilder:
    def __init__(self):
        self.personaje = Personaje()
    def set_name(self,name):
        self.personaje.name=name
    def set_level(self,level):
        self.personaje.level=level
    def set_role(self,role):
        self.personaje.role=role
    def set_charisma(self,charisma):
        self.personaje.charisma=charisma
    def set_strenght(self,strenght):
        self.personaje.strength=strenght
    def set_dexterity(self,dexteriry):
        self.personaje.dexterity=dexteriry
    def get_personaje(self):
        return self.personaje
    
    
class Videojuego:
    def __init__(self, builder):
        self.builder = builder

    def create_personaje(self,name,level,role,charisma,strenght,dexterity):
        self.builder.set_name(name)
        self.builder.set_level(level)
        self.builder.set_role(role)
        self.builder.set_charisma(charisma)
        self.builder.set_strenght(strenght)
        self.builder.set_dexterity(dexterity)
        return self.builder.get_personaje()
class VideojuegoService:
    def __init__(self):
        self.builder = PersonajeBuilder()
        self.videojuego = Videojuego(self.builder)

    def create_personaje(self, post_data):
        name=post_data.get("name",None)
        level = post_data("level",None)
        role = post_data("role",None)
        charisma= post_data("charisma",None)
        strenght = post_data("strenght",None)
        dexterity= post_data("dexterity",None)

        personaje = self.videojuego.create_personaje(name,level,role,charisma,strenght,dexterity)
        personajes[len(personajes) + 1] = personaje
        
        return personaje

    def read_personajes(self):
        return {index: personaje.__dict__ for index, personaje in personajes.items()}

    def update_personaje(self, index, data):
        if index in personajes:
            personaje = personajes[index]
            name = data.get("name",None)
            level= data.get("level",None)
            role = data.get("role",None)
            charisma = data.get("charisma",None)
            strenght = data.get("strenght",None)
            dexterity = data.get("dexterity",None)
            if name:
                personaje.name=name
            if level:
                personaje.level=level
            if role:
                personaje.role=role
            if charisma:
                personaje.charisma=charisma
            if strenght:
                personaje.strenght=strenght
            if dexterity:
                personaje.dexterity=dexterity
            return personaje
        else:
            return None

    def delete_personaje(self, index):
        if index in personajes:
            return personajes.pop(index)
        else:
            return None
class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))

class VideojuegoHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controller = VideojuegoService()
        super().__init__(*args, **kwargs)

    def do_POST(self):
        if self.path == "/chracters":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.create_personaje(data)
            HTTPDataHandler.handle_response(self, 201, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        if parsed_path.path == "/characters":
            if ("role" and "level" and "charisma") in query_params:
                role = query_params["role"][0]
                level = query_params["level"][0]
                charisma = query_params["charisma"][0]
                personajes_filtrados = VideojuegoService.filer(role,level,charisma)
                if personajes_filtrados!=[]:
                    HTTPDataHandler.handle_response(self,200,response_data)
                else:
                    HTTPDataHandler.handle_response(self,204,[])
            else:
                response_data = self.controller.read_personajes()
                HTTPDataHandler.handle_response(self,200,response_data)
        elif self.path.startswith("/characters/"):
            id = int(self.path.split("/")[-1])
            personaje = VideojuegoService.find_personaje(id)
            if personajes:
                HTTPDataHandler.handle_response(self,200,[personaje])
            else:
                HTTPDataHandler.handle_response(self,204,[])
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )        
                
                
            

    def do_PUT(self):
        if self.path.startswith("/characters/"):
            index = int(self.path.split("/")[2])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.update_personaje(index,data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "Índice de jugador no válido"}
                )
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/characters/"):
            index = int(self.path.split("/")[2])
            deleted_pizza = self.controller.delete_personaje(index)
            if deleted_pizza:
                HTTPDataHandler.handle_response(
                    self, 200, {"message": "Jugador eliminada correctamente"}
                )
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "Índice de jugador no válido"}
                )
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})


def run(server_class=HTTPServer, handler_class=VideojuegoHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor HTTP en puerto {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()































