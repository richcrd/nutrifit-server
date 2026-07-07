class DomainError(Exception):
  def __init__(self, message: str):
    self.message = message
    super().__init__(message)

class DiagnosticNotFound(DomainError):
  def __init__(self):
    super().__init__("No se encontro un diagnostico para los datos proporcionados")

class UserNotFound(DomainError):
  def __init__(self):
    super().__init__("Usuario no encontrado")

class InvalidCredentials(DomainError):
  def __init__(self):
    super().__init__("Credenciales invalidas")

class EmailRegistered(DomainError):
  def __init__(self):
    super().__init__("El email ya esta registrado")
