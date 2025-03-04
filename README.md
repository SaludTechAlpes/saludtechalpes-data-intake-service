# SaludTech Alpes - Data Intake Service

Este repositorio contiene el servicio de ingesta de datos para el proyecto **SaludTech Alpes**. Este servicio implementa una arquitectura basada en **eventos y comandos**, utilizando **CQRS** y separación de responsabilidades para garantizar modularidad y escalabilidad.

![Github](https://github.com/SaludTechAlpes/saludtechalpes-data-intake-service/actions/workflows/action.yaml/badge.svg)
![Github](https://github.com/SaludTechAlpes/saludtechalpes-data-intake-service/actions/workflows/merge-to-develop.yaml/badge.svg)
![Github](https://github.com/SaludTechAlpes/saludtechalpes-data-intake-service/actions/workflows/release-to-main.yaml/badge.svg)


## 📂 Estructura del Proyecto

El proyecto sigue una estructura modular organizada por capas de **Dominio, Aplicación e Infraestructura**, siguiendo los principios de **Domain-Driven Design (DDD)**. A continuación, se describe cada parte:

### **1.** **`src/config`**

Contiene la configuración del proyecto:

- `config.py`: Configuraciones generales de la aplicación.
- `db.py`: Configuración de la base de datos y conexión.

### **2.** **`src/modulos`**

Aquí se encuentran los módulos principales del sistema.

#### **2.1 `ingesta`**

Este módulo maneja la ingesta de datos antes de ser anonimizados. Según la arquitectura diseñada debería estar en un **microservicio separado**, pero para poder evidenciar el correcto funcionamiento de los otros módulos, se ha puesto temporalmente aqui. Sus principales componentes son:

- **`aplicacion`**: Contiene la lógica de aplicación y los servicios encargados de coordinar procesos de negocio.
- **`dominio`**: Define las entidades, reglas de negocio, eventos de dominio y puertos.
- **`infraestructura`**: Implementaciones concretas de los puertos, repositorios, adaptadores y consumidores de eventos.
- **`eventos.py`**: Define los eventos de dominio relacionados con la anonimización de datos.
- **`comandos.py`**: Define los comandos ejecutados dentro del proceso de anonimización.

### **3. `src/seedwork`**

Este módulo contiene código reutilizable para todas las aplicaciones dentro del sistema.

- **`aplicacion`**: Define servicios genéricos, comandos y handlers.
- **`dominio`**: Contiene las abstracciones de entidades, eventos, objetos de valor, reglas de negocio y repositorios.
- **`infraestructura`**: Define implementaciones genéricas de consumidores de eventos, repositorios y en general puertos.

## 🔄 **Flujo de Trabajo del Sistema**

El sistema sigue un flujo basado en **eventos y comandos**:

1. **Ingesta de datos**: El módulo de ingesta emite el evento **`DatosIngestadosEvento`**.
2. **Anonimización de datos**: El módulo de anonimización consume este evento y envía el comando **`AnonimizarDatosComando`**.
3. **Procesamiento de anonimización**: Se ejecuta el proceso de anonimización y, si es exitoso, se emite el evento **`DatosAnonimizadosEvento`**.
4. **Mapeo de datos**: El módulo de mapeo escucha **`DatosAnonimizadosEvento`** y ejecuta el comando **`MapearDatosComando`**, que agrupa las imágenes en clústeres según sus metadatos.
5. **Procesamiento de mapeo**: Se ejecuta el proceso de mapeo y, si es exitoso, se emite el evento **`DatosAgrupados`**

## 🚀 **Cómo Ejecutar la Aplicación**

### **1. Configuración previa (si no se usa Gitpod)**

Si no estás utilizando Gitpod, es necesario ejecutar los siguientes comandos antes de iniciar la aplicación para el correcto funcionamiento de Pulsar:

```bash
mkdir -p data/bookkeeper && mkdir -p data/zookeeper && sudo chmod -R 777 ./data
```

### **2. Desplegar con Docker Compose**

```bash
make docker-up
```
O si no tiene instalado make

```bash
docker-compose up --build
```

### **3. En caso de errores con Bookkeeper o Zookeeper**

Si los contenedores de **Bookkeeper** o **Zookeeper** fallan o se reinician constantemente, sigue estos pasos:

```bash
docker-compose down -v
rm -rf data
mkdir -p data/bookkeeper && mkdir -p data/zookeeper && sudo chmod -R 777 ./data
make docker-up
```

## 🛠 **Endpoints de la API**

### **1. Verificar estado del servicio**

**Endpoint:** `GET /health`

**Descripción:** Retorna el estado de la aplicación.

**Ejemplo de solicitud con curl:**

```bash
curl -X GET http://localhost:5000/health
```

**Respuesta:**

```json
{
  "status": "up",
  "application_name": "SaludTech Alpes",
  "environment": "development"
}
```

### **2. Simular ingesta de datos**

**Endpoint:** `GET /simular-ingesta-evento`

**Descripción:** Envía un evento de ingesta de datos ficticio a Pulsar, lo que comienza todo el proceso de anonimización y mapeo.

**Ejemplo de solicitud con curl:**

```bash
curl -X GET http://localhost:5000/simular-ingesta-evento
```

**Respuesta:**

```json
{
  "message": "Evento enviado a Pulsar"
}
```

## 📌 **Notas Finales**

Este servicio es solo una parte del sistema **SaludTech Alpes** y debe comunicarse con otros servicios para funcionar correctamente.

---