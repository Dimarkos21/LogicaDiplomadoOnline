# Corregir Duplicidad de cedulas y Identificador 
# Repaldo en un archivo tipo text.txt
# Cuello de botella en calculo de promedio y suma de notas
# Hacer Calculo Automatico de Promedio para dar la nota final
# Registrar Profesores 
# Registrar alumnos 
# Panel de opciones
# Estudiante pueda ver su propia Nota
# Profesor solo tiene acceso  a las notas de los estudiantes que le corresponden
# de lo contrario no tendra acceso 


# FUNCIONES X


def buscar_profesor(cedula_buscada):
    """Busca un profesor en profesores.txt por su cédula evitando duplicados y errores."""
    try:
        with open("profesores.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                partes = linea.strip().split(",")
                if len(partes) >= 1 and partes[0] == cedula_buscada:
                    return linea.strip()
    except FileNotFoundError:
        pass
    return None


def buscar_alumno(cedula_buscada):
    """Busca un alumno en alumnos.txt por su cédula evitando duplicados."""
    try:
        with open("alumnos.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                partes = linea.strip().split(",")
                if len(partes) >= 1 and partes[0] == cedula_buscada:
                    return linea.strip()
    except FileNotFoundError:
        pass
    return None




def registrar_profesor():
    """Opción 4: Director podrá agregar profesores verificando duplicidad de cédula."""
    print("\n--- REGISTRAR NUEVO PROFESOR (ACCESO DIRECTOR) ---")
    cedula = input("Ingrese la cédula del profesor: ").strip()
    
    # Corregir duplicidad de cédulas
    if buscar_profesor(cedula):
        print("❌ ¡Error! Ya existe un profesor registrado con esa cédula.")
        return

    nombre = input("Nombre del Profesor: ").strip()
    materia_curso = input("Materia o Curso que imparte (ej. Diplomado / Bootcamp / Curso): ").strip()

    nuevo_registro = f"{cedula},{nombre},{materia_curso}\n"
    
    # Respaldo y guardado en archivo de texto
    with open("profesores.txt", "a", encoding="utf-8") as archivo:
        archivo.write(nuevo_registro)
    
    print("¡Profesor registrado con éxito!")


def registrar_alumno(profesor_activo):
    """Registra o gestiona un alumno validando que pertenezca al curso/materia del profesor."""
    print("\n--- Registrar / Gestionar Alumno ---")
    
    # Extraer los datos del profesor activo para validar su materia asignada
    datos_prof = profesor_activo.split(",")
    materia_profesor = datos_prof[2].strip().lower() if len(datos_prof) > 2 else ""

    cedula = input("Cédula del Alumno: ").strip()
    resultado = buscar_alumno(cedula)
    
    if resultado:
        # El alumno ya existe, verificamos si corresponde al curso del profesor
        datos_alu = resultado.split(",")
        curso_alumno = datos_alu[3].strip().lower() if len(datos_alu) > 3 else ""
        
        if materia_profesor and materia_profesor not in curso_alumno and curso_alumno not in materia_profesor:
            print("❌ Profesor intenta modificar un alumno de otro curso (Permisos Insuficientes)")
            return
        
        print(f"Estudiante ya se encuentra registrado. Actualizando notas para: {datos_alu[1]}")
        try:
            n1 = float(input("Ingrese la Nueva Nota 1 (0 a 20): ").strip() or datos_alu[4])
            n2 = float(input("Ingrese la Nueva Nota 2 (0 a 20): ").strip() or datos_alu[5])
            n3 = float(input("Ingrese la Nueva Nota 3 (0 a 20): ").strip() or datos_alu[6])
            
            if not (0 <= n1 <= 20 and 0 <= n2 <= 20 and 0 <= n3 <= 20):
                print("❌ Error: Las notas deben estar entre 0 y 20.")
                return

            # Reescribir el archivo actualizando al alumno
            with open("alumnos.txt", "r", encoding="utf-8") as f:
                lineas = f.readlines()
            
            with open("alumnos.txt", "w", encoding="utf-8") as f:
                for linea in lineas:
                    if linea.startswith(cedula + ","):
                        f.write(f"{cedula},{datos_alu[1]},{datos_alu[2]},{datos_alu[3]},{n1},{n2},{n3}\n")
                    else:
                        f.write(linea)
            print("¡Notas actualizadas con éxito!")
        except ValueError:
            print("❌ Error: Debes ingresar un número válido.")
    else:
        # Registrar nuevo alumno
        nombre = input("Nombre del Alumno: ").strip()
        correo = input("Correo del Alumno: ").strip() 
        print("Seleccione el Tipo de Programa:")
        print("1. Diplomado")
        print("2. Bootcamp")
        print("3. Curso")
        curso_op = input("Opción (1-3): ").strip()
        
        valor = ""
        if curso_op == "1":
            valor = "Diplomado"
        elif curso_op == "2":
            valor = "Bootcamp"
        elif curso_op == "3":
            valor = "Curso"
        else:
            print("❌ Elige una opción válida.")
            return


        if materia_profesor and materia_profesor not in valor.lower() and valor.lower() not in materia_profesor:
            print("❌ Profesor intenta registrar un alumno en un curso que no le corresponde (Permisos Insuficientes)")
            return

        try:
            nota1 = float(input("Ingrese la Nota 1 del Alumno (o 0): ").strip() or 0)
            nota2 = float(input("Ingrese la Nota 2 del Alumno (o 0): ").strip() or 0)
            nota3 = float(input("Ingrese la Nota 3 del Alumno (o 0): ").strip() or 0)
            
            if not (0 <= nota1 <= 20 and 0 <= nota2 <= 20 and 0 <= nota3 <= 20):
                print("❌ Error: Las notas deben estar entre 0 y 20.")
                return

            # Guardar en archivo text respaldo
            nuevo_registro = f"{cedula},{nombre},{correo},{valor},{nota1},{nota2},{nota3}\n"
            with open("alumnos.txt", "a", encoding="utf-8") as archivo:
                archivo.write(nuevo_registro)
            print("¡Alumno registrado con éxito!")
             
        except ValueError:
            print("❌ Error: Debes ingresar un número válido (ej. 14.5). Operación cancelada.")
            return


def generar_cola_certificados():
    """Opción 5: Generacion  ."""
    print("\n--- GENERAR COLA DE CERTIFICADOS ---")
    try:
        cola_certificados = []
        
        with open("alumnos.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                partes = linea.strip().split(",")
                if len(partes) >= 7:
                    cedula, nombre, correo, curso = partes[0], partes[1], partes[2], partes[3]
                    try:
                        n1, n2, n3 = float(partes[4]), float(partes[5]), float(partes[6])
                        # Cálculo del Promedio 
                        promedio = (n1 + n2 + n3) / 3
                        
                        #  regla de aprobacion
                        if promedio >= 14.0:
                            cola_certificados.append({
                                "cedula": cedula,
                                "nombre": nombre,
                                "curso": curso,
                                "promedio": promedio
                            })
                    except ValueError:
                        continue

        print(f"\nTotal de graduandos en cola: {len(cola_certificados)}")
        
        if len(cola_certificados) == 0:
            print("No hay alumnos aprobados en este momento.")
            return

        # Procesar la cola en orden FIFO usando pop(0)
        contador = 1
        print("\n=========================================")
        print("LISTA DE CERTIFICADOS PENDIENTES (FIFO)")
        print("=========================================")
        while len(cola_certificados) > 0:
            graduando = cola_certificados.pop(0)
            print(f"{contador}. [{graduando['cedula']}] {graduando['nombre']} | Curso: {graduando['curso']} | Promedio Final: {round(graduando['promedio'], 1)} (APROBADO 🎓)")
            contador += 1
        print("=========================================")

    except FileNotFoundError:
        print("El archivo alumnos.txt aún no existe. Registra alumnos primero.")


def mostrar_reporte_general():
    """Opción 6: Mostrar Reporte General de Profesores y Alumnos con cálculo de promedio."""
    print("\n============================================")
    print("6. REPORTE GENERAL DEL SISTEMA ")
    print("==================================================")
    
    print("\n--- PROFESORES REGISTRADOS ---")
    try:
        with open("profesores.txt", "r", encoding="utf-8") as f:
            for linea in f:
                p = linea.strip().split(",")
                if len(p) >= 3:
                    print(f"Cédula: {p[0]} | Nombre: {p[1]} | Materia/Curso: {p[2]}")
    except FileNotFoundError:
        print("No hay profesores registrados.")

    print("\n--- ALUMNOS REGISTRADOS ---")
    try:
        with open("alumnos.txt", "r", encoding="utf-8") as f:
            for linea in f:
                p = linea.strip().split(",")
                if len(p) >= 7:
                    try:
                        n1, n2, n3 = float(p[4]), float(p[5]), float(p[6])
                        promedio = (n1 + n2 + n3) / 3
                        print(f"Cédula: {p[0]} | Nombre: {p[1]} | Curso: {p[3]} | Promedio: {round(promedio, 1)}")
                    except ValueError:
                        print(f"Cédula: {p[0]} | Nombre: {p[1]} | Error en notas")
    except FileNotFoundError:
        print("No hay alumnos registrados.")
    print("==================================================")


# ==========================================
# MENÚ PRINCIPAL
# ==========================================

def gestionar_ingreso():
    """Controla el menú principal del sistema ."""
    while True:
        opcion = input("""
==================================================
: SISTEMA DIPLOMADOSONLINE
==================================================
1. Ingresar como Profesor (Gestionar notas de mis alumnos)
2. Ingresar como Alumno (Ver mi nota y estatus)
3. Registrar Nuevo Alumno
4. Registrar Nuevo Profesor (Acceso Director)
5. Generar Cola de Certificados
6. Mostrar Reporte General
7. Salir
==================================================
Seleccione una opción (1-7): """).strip()

        if opcion == "1":
            cedula = input("Ingrese su cédula de profesor: ").strip()
            data = buscar_profesor(cedula)

            if not data:
                print("❌ Profesor no registrado.")
                continue

            datos = data.split(",")
            print(f"Bienvenido Profesor {datos[1]} de {datos[2]} con cédula {datos[0]}")
            
            # Pasar profesor activo para validar sus permisos
            registrar_alumno(data)

        elif opcion == "2":
            cedula = input("Ingrese su cédula de alumno: ").strip()
            data = buscar_alumno(cedula)

            if not data:
                print("❌ Alumno no encontrado.")
                continue

            datos = data.split(",")
            print(f"\nBienvenido Alumno {datos[1]} de {datos[3]} con cédula {datos[0]}")

            try:
                n1, n2, n3 = float(datos[4]), float(datos[5]), float(datos[6])
                promedio = (n1 + n2 + n3) / 3
                print(f"Tus notas: Nota 1: {n1} | Nota 2: {n2} | Nota 3: {n3}")
                print(f"Tu promedio final es: {round(promedio, 1)}")
                
                if promedio >= 14.0:
                    print("Felicidades, Aprobaste 🎓")
                else:
                    print("No aprobaste ❌")
            except ValueError:
                print("❌ Error al leer las notas del alumno.")

        elif opcion == "3":
            cedula = input("Profesor ingrese su Cédula para autorizar: ").strip()
            prof_data = buscar_profesor(cedula)
            if prof_data:
                registrar_alumno(prof_data)
            else:
                print("❌ Profesor no autorizado o no registrado.")

        elif opcion == "4":
            registrar_profesor()

        elif opcion == "5":
            generar_cola_certificados()

        elif opcion == "6":
            mostrar_reporte_general()

        elif opcion == "7":
            print("\nTerminó el Proceso. ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida. Seleccione un número del 1 al 7.")


# Ejecución del programa
if __name__ == "__main__":
    gestionar_ingreso()