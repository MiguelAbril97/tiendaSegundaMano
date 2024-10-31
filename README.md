# tiendaSegundaMano
El proyecto representa una tienda de segunda mano en la que los usuarios son compradores y vendedores. Pueden no tener un producto en venta, uno o mas de un producto. Los usuarios pueden interactuar entre ellos mediante chats. Las compras pueden ser de mas de un producto. 


modelo Usuario:
Almacenara todos los usuarios que usen nuestra aplicacion. En el campo correo_electronico uso EmailField para que valide automaticamente el formato de los correos.  unique=True hace que no se puedan repetir 2 correos iguales

modelo Categoria
recogera todas las categorias de productos que habra en la plataforma (por ejemplo: entretenimiento, decoracion, electronica, etc). en el campo descripcion uso blank=true para que no sea obligatorio añadirle una descripcion

modelo Producto
todos los productos iran aqui. Contiene toda la informacion que es comun a todos los productos que haya

modelo Calzado
contiene la informacion especifica que tendran todos calzados que se vendan. Uso choices para marcas aunque no se la mejor opcion por variar simplemente

modelo Consolas
contiene la informacion especifica que tendran todas las consolas que se vendan

modelo Muebles
contiene la informacion especifica que tendran todos los muebles que se vendan. Separo las dimensiones para que se puedan hacer mejor los filtros en un futuro. Asi podria filtrarse mejor la busqueda por ejemplo, por alutura

modelo Chat
contiene las conversaciones entre usuarios. Se recoge la fecha de inicio y la fecha en la que se finaliza la conversacion.
historial: el chat completo
reporte: simulando un reporte a un usuario por una conversacion 

modelo Compra
contiene el total de una compra que haga el usuario. Uso decimalField para determinar que haya solo 2 decimales

modelo CompraProducto
idica cada producto individual de una compra y el subtotal. No añado el id del vendedor porque ya esta en el registro del producto

modelo Envio
registra la informacion necesaria para cada envio. Esta el campo direccion porque el usuario puede pedir que se envie a otra direccion

modelo Valoracion
Los usuarios pueden dejar valoraciones sobre las compras hechas. Dejo comentario siendo opcional con blank True

URLS
1 Muestra un indice para probar las demas url
