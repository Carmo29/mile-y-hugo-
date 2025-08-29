#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ejemplo práctico de sistema de gestión hotelera en Python
Demuestra cómo Python puede ser útil para empresas hoteleras
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional

class Habitacion:
    """Representa una habitación del hotel"""
    def __init__(self, numero: int, tipo: str, precio_noche: float):
        self.numero = numero
        self.tipo = tipo  # "individual", "doble", "suite"
        self.precio_noche = precio_noche
        self.disponible = True
        self.mantenimiento = False

class Huesped:
    """Representa un huésped del hotel"""
    def __init__(self, nombre: str, email: str, telefono: str):
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.historial_reservas = []

class Reserva:
    """Representa una reserva en el hotel"""
    def __init__(self, huesped: Huesped, habitacion: Habitacion, 
                 fecha_entrada: datetime, fecha_salida: datetime):
        self.huesped = huesped
        self.habitacion = habitacion
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.noches = (fecha_salida - fecha_entrada).days
        self.precio_total = self.noches * habitacion.precio_noche
        self.confirmada = False

class SistemaHotel:
    """Sistema principal de gestión hotelera"""
    
    def __init__(self, nombre_hotel: str):
        self.nombre_hotel = nombre_hotel
        self.habitaciones: List[Habitacion] = []
        self.huespedes: List[Huesped] = []
        self.reservas: List[Reserva] = []
        self.ingresos_totales = 0.0
    
    def agregar_habitacion(self, numero: int, tipo: str, precio: float):
        """Agrega una nueva habitación al hotel"""
        habitacion = Habitacion(numero, tipo, precio)
        self.habitaciones.append(habitacion)
        print(f"Habitación {numero} ({tipo}) agregada - ${precio}/noche")
    
    def registrar_huesped(self, nombre: str, email: str, telefono: str) -> Huesped:
        """Registra un nuevo huésped"""
        huesped = Huesped(nombre, email, telefono)
        self.huespedes.append(huesped)
        print(f"Huésped {nombre} registrado exitosamente")
        return huesped
    
    def buscar_habitaciones_disponibles(self, fecha_entrada: datetime, 
                                      fecha_salida: datetime, tipo: str = None) -> List[Habitacion]:
        """Busca habitaciones disponibles para las fechas especificadas"""
        disponibles = []
        
        for habitacion in self.habitaciones:
            if habitacion.mantenimiento:
                continue
                
            # Verificar si hay conflictos con reservas existentes
            conflicto = False
            for reserva in self.reservas:
                if (reserva.habitacion.numero == habitacion.numero and
                    reserva.confirmada and
                    not (fecha_salida <= reserva.fecha_entrada or 
                         fecha_entrada >= reserva.fecha_salida)):
                    conflicto = True
                    break
            
            if not conflicto and (tipo is None or habitacion.tipo == tipo):
                disponibles.append(habitacion)
        
        return disponibles
    
    def hacer_reserva(self, huesped: Huesped, numero_habitacion: int,
                     fecha_entrada: datetime, fecha_salida: datetime) -> Optional[Reserva]:
        """Crea una nueva reserva"""
        # Buscar la habitación
        habitacion = next((h for h in self.habitaciones if h.numero == numero_habitacion), None)
        if not habitacion:
            print(f"Error: Habitación {numero_habitacion} no existe")
            return None
        
        # Verificar disponibilidad
        disponibles = self.buscar_habitaciones_disponibles(fecha_entrada, fecha_salida)
        if habitacion not in disponibles:
            print(f"Error: Habitación {numero_habitacion} no disponible para las fechas solicitadas")
            return None
        
        # Crear reserva
        reserva = Reserva(huesped, habitacion, fecha_entrada, fecha_salida)
        reserva.confirmada = True
        self.reservas.append(reserva)
        huesped.historial_reservas.append(reserva)
        
        print(f"Reserva confirmada:")
        print(f"  Huésped: {huesped.nombre}")
        print(f"  Habitación: {habitacion.numero} ({habitacion.tipo})")
        print(f"  Fechas: {fecha_entrada.strftime('%Y-%m-%d')} a {fecha_salida.strftime('%Y-%m-%d')}")
        print(f"  Noches: {reserva.noches}")
        print(f"  Total: ${reserva.precio_total}")
        
        return reserva
    
    def check_in(self, numero_habitacion: int) -> bool:
        """Proceso de check-in"""
        reserva = next((r for r in self.reservas 
                       if r.habitacion.numero == numero_habitacion and 
                       r.confirmada and
                       r.fecha_entrada.date() <= datetime.now().date()), None)
        
        if reserva:
            print(f"Check-in exitoso - Habitación {numero_habitacion}")
            print(f"Bienvenido/a {reserva.huesped.nombre}")
            return True
        else:
            print(f"Error: No se encontró reserva válida para habitación {numero_habitacion}")
            return False
    
    def check_out(self, numero_habitacion: int) -> bool:
        """Proceso de check-out"""
        reserva = next((r for r in self.reservas 
                       if r.habitacion.numero == numero_habitacion and 
                       r.confirmada), None)
        
        if reserva:
            self.ingresos_totales += reserva.precio_total
            print(f"Check-out exitoso - Habitación {numero_habitacion}")
            print(f"Factura: ${reserva.precio_total}")
            print(f"Gracias por su estadía, {reserva.huesped.nombre}")
            return True
        else:
            print(f"Error: No se encontró reserva para habitación {numero_habitacion}")
            return False
    
    def reporte_ocupacion(self) -> Dict:
        """Genera reporte de ocupación actual"""
        total_habitaciones = len(self.habitaciones)
        ocupadas = 0
        en_mantenimiento = 0
        
        hoy = datetime.now().date()
        
        for habitacion in self.habitaciones:
            if habitacion.mantenimiento:
                en_mantenimiento += 1
                continue
                
            # Verificar si está ocupada hoy
            for reserva in self.reservas:
                if (reserva.habitacion.numero == habitacion.numero and
                    reserva.confirmada and
                    reserva.fecha_entrada.date() <= hoy < reserva.fecha_salida.date()):
                    ocupadas += 1
                    break
        
        disponibles = total_habitaciones - ocupadas - en_mantenimiento
        porcentaje_ocupacion = (ocupadas / total_habitaciones) * 100 if total_habitaciones > 0 else 0
        
        reporte = {
            'total_habitaciones': total_habitaciones,
            'ocupadas': ocupadas,
            'disponibles': disponibles,
            'en_mantenimiento': en_mantenimiento,
            'porcentaje_ocupacion': round(porcentaje_ocupacion, 2),
            'ingresos_totales': self.ingresos_totales
        }
        
        return reporte
    
    def mostrar_reporte(self):
        """Muestra el reporte de ocupación"""
        reporte = self.reporte_ocupacion()
        print(f"\n--- REPORTE DE OCUPACIÓN - {self.nombre_hotel} ---")
        print(f"Total de habitaciones: {reporte['total_habitaciones']}")
        print(f"Habitaciones ocupadas: {reporte['ocupadas']}")
        print(f"Habitaciones disponibles: {reporte['disponibles']}")
        print(f"En mantenimiento: {reporte['en_mantenimiento']}")
        print(f"Porcentaje de ocupación: {reporte['porcentaje_ocupacion']}%")
        print(f"Ingresos totales: ${reporte['ingresos_totales']}")


def ejemplo_uso():
    """Ejemplo de uso del sistema hotelero"""
    print("=== SISTEMA DE GESTIÓN HOTELERA ===")
    
    # Crear hotel
    hotel = SistemaHotel("Hotel Coralina")
    
    # Agregar habitaciones
    hotel.agregar_habitacion(101, "individual", 80.0)
    hotel.agregar_habitacion(102, "doble", 120.0)
    hotel.agregar_habitacion(201, "suite", 200.0)
    hotel.agregar_habitacion(202, "doble", 120.0)
    
    print("\n--- REGISTRO DE HUÉSPEDES ---")
    # Registrar huéspedes
    huesped1 = hotel.registrar_huesped("María García", "maria@email.com", "555-0001")
    huesped2 = hotel.registrar_huesped("Carlos López", "carlos@email.com", "555-0002")
    
    print("\n--- BÚSQUEDA DE HABITACIONES ---")
    # Buscar habitaciones disponibles
    fecha_entrada = datetime.now() + timedelta(days=1)
    fecha_salida = datetime.now() + timedelta(days=4)
    
    disponibles = hotel.buscar_habitaciones_disponibles(fecha_entrada, fecha_salida)
    print(f"Habitaciones disponibles del {fecha_entrada.strftime('%Y-%m-%d')} al {fecha_salida.strftime('%Y-%m-%d')}:")
    for hab in disponibles:
        print(f"  - Habitación {hab.numero} ({hab.tipo}) - ${hab.precio_noche}/noche")
    
    print("\n--- HACER RESERVAS ---")
    # Hacer reservas
    hotel.hacer_reserva(huesped1, 101, fecha_entrada, fecha_salida)
    hotel.hacer_reserva(huesped2, 201, fecha_entrada, fecha_salida)
    
    print("\n--- PROCESO CHECK-IN ---")
    # Simular check-in
    hotel.check_in(101)
    hotel.check_in(201)
    
    # Mostrar reporte
    hotel.mostrar_reporte()
    
    print("\n--- PROCESO CHECK-OUT ---")
    # Simular check-out
    hotel.check_out(101)
    hotel.check_out(201)
    
    # Reporte final
    hotel.mostrar_reporte()


if __name__ == "__main__":
    ejemplo_uso()