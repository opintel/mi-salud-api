# API ML RAPIDPRO

El API proporciona servicios de etiquetado de mensajes para Rapid Pro. Tambien tiene capacidad
de aministriación de modelos asociados a distinto chatbots.

# Requerimientos
- [Python 3.5+](https://python.org/)
- [Django 2.1](https://www.djangoproject.com/)
- [Postgres](https://www.postgresql.org/)
- [mi-salud-ml](https://github.com/opintel/mi-salud)

# Endpoints
## Filtrado de mensajes
Descripción:

Endpoint diseñado para reconocer si el mensaje que entró al flujo es relevante
dentro del modelo y del flujo. Discrimina en base al contenido de mensaje, dejando fuera
aquellos mensajes cuyo contenido pueda ser identificado como:
- Ok.
- Emoji.
- Saludos/Despedida.
- Like Facebook.
- Links externos.

Detalles técnicos:

- **URL:** `/opi/pre-model-rules/bot/<int:id_modelo>/`
- **Metodos HTTP:** GET
- **Parametros:**

| Nombre | Metodo | Tipo | Obligatorio | Descripción |
|---|---|---|---|---|
| message | GET | String | Si | Mensaje de texto que se desea filtrar |
| id_rp_user | GET | String | Si | Id del usuario que emite el mensaje |
|   |   |   |   |   |

- **Formato de respuesta:** JSON.
- **Estructura de mensaje:**
```sh
{
    "pre_category": "ok"
}
```

## Estado del modelo
Descripción:

Endpoint diseñado para exponer a la plataforma Rapid Pro el estado del modelo. El estado del modelo esta representado con la bandera `training`:
- En entrenamiento: `true`
- Productivo: `false`

Detalles técnicos:

- **URL:** `/opi/model-is-in-training/bot/<int:id_modelo>/`
- **Metodos HTTP:** GET
- **Formato de respuesta:** JSON.
- **Estructura de mensaje:**
```sh
{
    "training": true
}
```

## Etiquetado

Descripción:

Endpoint diseñado para etiquetar mensajes dependiendo del estado del modelo. Si el modelo se encuentra en entrenamiento se guardara la etiqueta del mensaje asignada por el mismo usuario. En caso de que el modelo se encuentre productivo, el modelo asignara una etiqueta al mensaje y guardara el resultado en la base de datos.

Detalles técnicos:

- **URL:** `/opi/tag-new-message/bot/<int:id_modelo>/`
- **Metodos HTTP:** GET
- **Parametros:**

| Nombre | Metodo | Tipo | Obligatorio | Descripción |
|---|---|---|---|---|
| message | GET | String | Si | Mensaje de texto que se desea filtrar |
| id_rp_user | GET | String | Si | Id del usuario que emite el mensaje |
| user_tag | GET | String  | No | Etiqueta asiganada por el usuario al mensaje evaluado |

- **Formato de respuesta:** JSON.
- **Estructura de mensaje:**
```sh
{
    "category": "pregunta"
}
```

# Administración

## Bots
El API ML para Rapid Pro cuenta con un pane de administración de modelos asociados a los bots de la plataforma.

### Ingreso al panel de Administración

1. Navegar a `/opi/admin/`.
2. Ingresar los datos en los campos de **usuario** y **password**.
3. Click en boton ingresar.

### Crear Modelo/Bot

1. Navegar a `/opi/admin/bots/bot/add/`.
2. Ingresar el nombre del modelo en el campo `Name`.
3. No cambiar el valor del campo `Token`.
4. Activar el campo `Enable` para que el modelo quede activado.
5. Desactivar el campo `Is in training`.
6. Agregar las categorias que va a clasificar el modelo en la sección `BOT-CATEGORY RELATIONSHIPS`.
7. Click en el botón `Save`.
![bot-panel.png](/docs/new-bot.png)

### Cambio de estado de Modelo/Bot

1. Navegar a `/opi/admin/bots/bot/`.
2. Click en el modelo a modificar de la lista de que aparece en la tabla.
![bot-panel.png](/docs/bot-panel.png)
3. Cambiar el estado del campo `Is in training` a activado si esta en entrenamiento, de lo contrario para casos productivos dejar desactivado.
4. Click en el botón `Save`.