window.addEventListener('load',inicializar);
var nombre, apellidos, razon, dirFiscal;
var rol;
function inicializar(){
    rol = document.getElementById('id_rol');
    rol.addEventListener('click',mostrar);

    nombre = document.getElementById('id_nombre');
    nombreLabel = nombre.previousElementSibling;

    apellidos = document.getElementById('id_apellidos');
    apellidosLabel = apellidos.previousElementSibling;

    razon = document.getElementById('id_razonSocial');
    razonLabel = razon.previousElementSibling;  
    
    dirFiscal = document.getElementById('id_direccionFiscal');
    dirFiscalLabel = dirFiscal.previousElementSibling;

    nombre.style.display = 'none';
    nombreLabel.style.display = 'none';

    apellidos.style.display = 'none';
    apellidosLabel.style.display = 'none';

    razon.style.display = 'none';
    razonLabel.style.display = 'none';

    dirFiscal.style.display = 'none';
    dirFiscalLabel.style.display = 'none';

}

function mostrar(){
    if(rol.value == '2'){
        nombre.style.display = 'block';
        nombreLabel.style.display = 'block';
    
        apellidos.style.display = 'block';
        apellidosLabel.style.display = 'block';
    

        razon.style.display = 'none';
        razonLabel.style.display = 'none';
    
        dirFiscal.style.display = 'none';
        dirFiscalLabel.style.display = 'none';

    }else if(rol.value == '3'){
        razon.style.display = 'block'
        razonLabel.style.display = 'block';

        dirFiscal.style.display = 'block'
        dirFiscalLabel.style.display = 'block';

        nombre.style.display = 'none';
        nombreLabel.style.display = 'none';
    
        apellidos.style.display = 'none';
        apellidosLabel.style.display = 'none';
        
    }else{
        nombre.style.display = 'none';
        nombreLabel.style.display = 'none';
    
        apellidos.style.display = 'none';
        apellidosLabel.style.display = 'none';
    
        razon.style.display = 'none';
        razonLabel.style.display = 'none';
    
        dirFiscal.style.display = 'none';
        dirFiscalLabel.style.display = 'none';
    }
}
