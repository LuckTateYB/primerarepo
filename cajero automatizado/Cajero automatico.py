# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 10:04:36 2024
@author: Oscar
"""

import getpass
from datetime import datetime

class Usuario:
    def __init__(self, nombre, pin, saldo_inicial=0):
        self.nombre = nombre
        self.pin = pin
        self.saldo = saldo_inicial
        self.historial = []  

    def consultar_saldo(self):
        print(f"Su saldo actual es: ${self.saldo}")

    def depositar(self, cantidad, billetes):
        if cantidad > 0:
            self.saldo += cantidad
            id_operacion = f"{id(self)}_{len(self.historial)+1}"
            self.historial.append((id_operacion, datetime.now(), "Depositó", cantidad))
            print(f"Ha depositado: ${cantidad}")
            print(f"Billetes recibidos: {billetes}")
        else:
            print("La cantidad a depositar debe ser mayor a 0")

    def retirar(self, cantidad, billetes):
        if cantidad > 0:
            if cantidad <= self.saldo:
                self.saldo -= cantidad
                id_operacion = f"{id(self)}_{len(self.historial)+1}"
                self.historial.append((id_operacion, datetime.now(), "Retiró", cantidad))
                print(f"Ha retirado: ${cantidad}")
                print(f"Billetes entregados: {billetes}")
            else:
                print("Fondos insuficientes")
        else:
            print("La cantidad a retirar debe ser mayor a 0")

    def transferir(self, cantidad, destinatario):
        if cantidad > 0:
            if cantidad <= self.saldo:
                self.saldo -= cantidad
                destinatario.saldo += cantidad
                id_operacion = f"{id(self)}_{len(self.historial)+1}"
                self.historial.append((id_operacion, datetime.now(), f"Transfirió a {destinatario.nombre}", cantidad))
                id_operacion_destinatario = f"{id(destinatario)}_{len(destinatario.historial)+1}"
                destinatario.historial.append((id_operacion_destinatario, datetime.now(), f"Recibió de {self.nombre}", cantidad))
                print(f"Ha transferido: ${cantidad} a {destinatario.nombre}")
            else:
                print("Fondos insuficientes")
        else:
            print("La cantidad a transferir debe ser mayor a 0")

    def pagar_servicio(self, cantidad, servicio):
        if cantidad > 0:
            if cantidad <= self.saldo:
                self.saldo -= cantidad
                id_operacion = f"{id(self)}_{len(self.historial)+1}"
                self.historial.append((id_operacion, datetime.now(), f"Pagó {servicio}", cantidad))
                print(f"Ha pagado: ${cantidad} por {servicio}")
            else:
                print("Fondos insuficientes")
        else:
            print("La cantidad a pagar por servicio debe ser mayor a 0")

    def mostrar_historial(self):
        if self.historial:
            print("Historial de transacciones:")
            for id_operacion, fecha, operacion, monto in self.historial:
                print(f"- ID: {id_operacion} - {fecha}: {operacion} ${monto}")
        else:
            print("No hay transacciones en el historial.")

    def cambiar_pin(self, nuevo_pin):
        self.pin = nuevo_pin
        print("El PIN ha sido cambiado exitosamente.")

class CajeroAutomatico:
    def __init__(self):
        self.usuarios = {}
        self.dinero_disponible = {
            200: 10,  
            100: 20,
            50: 30,
            20: 50,
            10: 100,
            5: 200,
            1: 500
        }
        self.denominaciones = sorted(self.dinero_disponible.keys(), reverse=True)

    def agregar_usuario(self, nombre, pin, saldo_inicial=0):
        if nombre in self.usuarios:
            print("El nombre de usuario ya existe. Por favor, elija otro.")
        else:
            self.usuarios[nombre] = Usuario(nombre, pin, saldo_inicial)
            print(f"Usuario {nombre} creado exitosamente.")

    def autenticar_usuario(self, nombre, pin):
        usuario = self.usuarios.get(nombre)
        if usuario and usuario.pin == pin:
            return usuario
        else:
            print("Nombre de usuario o PIN incorrectos.")
            return None

    def ordenar_denominaciones(self):
        # Método de ordenamiento por burbuja
        n = len(self.denominaciones)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.denominaciones[j] < self.denominaciones[j+1]:
                    self.denominaciones[j], self.denominaciones[j+1] = self.denominaciones[j+1], self.denominaciones[j]

    def descomponer_billetes(self, monto):
        denominaciones_utilizadas = []
        self.ordenar_denominaciones()
        for denominacion in self.denominaciones:
            contador = 0
            while monto >= denominacion and self.dinero_disponible[denominacion] > 0:
                monto -= denominacion
                self.dinero_disponible[denominacion] -= 1
                contador += 1
            if contador > 0:
                denominaciones_utilizadas.append((denominacion, contador))
        if monto > 0:
            print("No se pudo completar la transacción debido a la falta de billetes.")
            self.reponer_billetes(denominaciones_utilizadas)
            denominaciones_utilizadas = []
        return denominaciones_utilizadas

    def reponer_billetes(self, denominaciones_utilizadas):
        for denominacion, cantidad in denominaciones_utilizadas:
            self.dinero_disponible[denominacion] += cantidad

    def actualizar_saldo(self, usuario, monto, tipo, billetes=None):
        if tipo == 'deposito':
            usuario.depositar(monto, billetes)
        elif tipo == 'retiro':
            if monto <= sum(self.dinero_disponible.values()):
                billetes_utilizados = self.descomponer_billetes(monto)
                if sum([cantidad for _, cantidad in billetes_utilizados]) > 0:
                    usuario.retirar(monto, billetes_utilizados)
                else:
                    print("No hay suficientes billetes en el dispensador para realizar esta operación.")
            else:
                print("Fondos insuficientes en el ATM.")
        elif tipo == 'transferencia':
            destinatario = self.usuarios.get(billetes)
            if destinatario:
                usuario.transferir(monto, destinatario)
            else:
                print("Destinatario no encontrado.")
        elif tipo == 'servicio':
            usuario.pagar_servicio(monto, billetes)  
        else:
            print("Tipo de transacción no reconocido.")

    def menu_usuario(self, usuario):
        while True:
            print(f"\n--- Menú Cajero Automático para {usuario.nombre} ---")
            print("1. Consultar saldo")
            print("2. Depositar dinero")
            print("3. Retirar dinero")
            print("4. Transferir dinero")
            print("5. Pagar servicio")
            print("6. Ver historial de transacciones")
            print("7. Cambiar PIN")
            print("8. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                usuario.consultar_saldo()
            elif opcion == "2":
                cantidad = float(input("Ingrese la cantidad a depositar: "))
                billetes = {}
                for denominacion in self.denominaciones:
                    cantidad_denom = int(input(f"Ingrese la cantidad de billetes de ${denominacion}: "))
                    billetes[denominacion] = cantidad_denom
                self.actualizar_saldo(usuario, cantidad, 'deposito', billetes)
            elif opcion == "3":
                cantidad = float(input("Ingrese la cantidad a retirar: "))
                self.actualizar_saldo(usuario, cantidad, 'retiro')
            elif opcion == "4":
                destinatario_nombre = input("Ingrese el nombre del destinatario: ")
                cantidad = float(input("Ingrese la cantidad a transferir: "))
                self.actualizar_saldo(usuario, cantidad, 'transferencia', destinatario_nombre)
            elif opcion == "5":
                print("Seleccione el servicio a pagar:")
                print("1. Internet")
                print("2. Luz")
                print("3. Agua")
                opcion_servicio = input("Seleccione una opción: ")
                if opcion_servicio == "1":
                    servicio = "Internet"
                elif opcion_servicio == "2":
                    servicio = "Luz"
                elif opcion_servicio == "3":
                    servicio = "Agua"
                else:
                    print("Opción no válida.")
                    continue
                cantidad = float(input(f"Ingrese la cantidad a pagar por {servicio}: "))
                self.actualizar_saldo(usuario, cantidad, 'servicio', servicio)
            elif opcion == "6":
                usuario.mostrar_historial()
            elif opcion == "7":
                nuevo_pin = getpass.getpass("Ingrese el nuevo PIN: ")
                usuario.cambiar_pin(nuevo_pin)
            elif opcion == "8":
                print("Gracias por usar el cajero automático. ¡Hasta luego!")
                break
            else:
                print("Opción no válida, por favor seleccione una opción válida.")

    def menu_administrador(self):
        while True:
            print(f"\n--- Menú Administrador ---")
            print("1. Agregar usuario")
            print("2. Editar información de usuario")
            print("3. Buscar usuario")
            print("4. Listar usuarios")
            print("5. Ordenar usuarios por saldo")
            print("6. Dar de baja usuario")
            print("7. Dispensador de billetes")
            print("8. Cerrar sesión")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                nombre = input("Ingrese el nombre de usuario: ")
                pin = getpass.getpass("Ingrese el PIN: ")
                saldo_inicial = float(input("Ingrese el saldo inicial: "))
                self.agregar_usuario(nombre, pin, saldo_inicial)
            elif opcion == "2":
                nombre = input("Ingrese el nombre de usuario a editar: ")
                usuario = self.usuarios.get(nombre)
                if usuario:
                    nuevo_nombre = input("Ingrese el nuevo nombre de usuario: ")
                    nuevo_pin = getpass.getpass("Ingrese el nuevo PIN: ")
                    usuario.nombre = nuevo_nombre
                    usuario.pin = nuevo_pin
                    self.usuarios[nuevo_nombre] = self.usuarios.pop(nombre)
                    print(f"Usuario {nombre} editado exitosamente.")
                else:
                    print("Usuario no encontrado.")
            elif opcion == "3":
                nombre = input("Ingrese el nombre de usuario a buscar: ")
                usuario = self.usuarios.get(nombre)
                if usuario:
                    print(f"Usuario encontrado: {usuario.nombre}, Saldo: ${usuario.saldo}")
                else:
                    print("Usuario no encontrado.")
            elif opcion == "4":
                print("Lista de usuarios:")
                for usuario in self.usuarios.values():
                    print(f"- {usuario.nombre}: ${usuario.saldo}")
            elif opcion == "5":
                print("Usuarios ordenados por saldo:")
                usuarios_ordenados = sorted(self.usuarios.values(), key=lambda x: x.saldo, reverse=True)
                for usuario in usuarios_ordenados:
                    print(f"- {usuario.nombre}: ${usuario.saldo}")
            elif opcion == "6":
                nombre = input("Ingrese el nombre de usuario a dar de baja: ")
                if nombre in self.usuarios:
                    del self.usuarios[nombre]
                    print(f"Usuario {nombre} eliminado exitosamente.")
                else:
                    print("Usuario no encontrado.")
            elif opcion == "7":
                denominacion = int(input("Ingrese la denominación del billete a reponer: "))
                cantidad = int(input("Ingrese la cantidad de billetes a reponer: "))
                if denominacion in self.dinero_disponible:
                    self.dinero_disponible[denominacion] += cantidad
                    print(f"Se han repuesto {cantidad} billetes de ${denominacion}.")
                else:
                    print("Denominación no válida.")
            elif opcion == "8":
                print("Saliendo del menú de administrador.")
                break
            else:
                print("Opción no válida, por favor seleccione una opción válida.")

def main():
    cajero = CajeroAutomatico()

    while True:
        print("\n--- Bienvenido al Cajero Automático ---")
        print("1. Cliente")
        print("2. Administrador")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\n--- Menú Cliente ---")
            print("1. Crear nuevo usuario")
            print("2. Iniciar sesión")
            print("3. Salir")

            opcion_cliente = input("Seleccione una opción: ")

            if opcion_cliente == "1":
                nombre = input("Ingrese su nombre de usuario: ")
                pin = getpass.getpass("Ingrese su PIN: ")
                saldo_inicial = float(input("Ingrese su saldo inicial: "))
                cajero.agregar_usuario(nombre, pin, saldo_inicial)
            elif opcion_cliente == "2":
                nombre = input("Ingrese su nombre de usuario: ")
                pin = getpass.getpass("Ingrese su PIN: ")
                usuario = cajero.autenticar_usuario(nombre, pin)
                if usuario:
                    cajero.menu_usuario(usuario)
            elif opcion_cliente == "3":
                print("Gracias por usar el cajero automático. ¡Hasta luego!")
            else:
                print("Opción no válida, por favor seleccione una opción válida.")

        elif opcion == "2":
            admin_pin = getpass.getpass("Ingrese el PIN de administrador: ")
            if admin_pin == "222":
                cajero.menu_administrador()
            else:
                print("PIN de administrador incorrecto.")
                
        elif opcion == "3":
            print("Gracias por usar el cajero automático. ¡Hasta luego!")
            break
        else:
            print("Opción no válida, por favor seleccione una opción válida.")

if __name__ == "__main__":
    main()

