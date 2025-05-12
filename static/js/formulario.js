function toggleOtroTema() {
    const select = document.getElementById("tema");
    const campo = document.getElementById("campo_otro_tema");
    campo.style.display = select.value === "otro" ? "block" : "none";
}

function filtrarComunas() {
    const regionId = document.getElementById("region_id").value;
    const comunaSelect = document.getElementById("comuna_id");
    const options = comunaSelect.querySelectorAll("option");

    options.forEach(option => {
        const pertenece = option.getAttribute("data-region");
        if (!pertenece || pertenece === regionId) {
            option.style.display = "block";
        } else {
            option.style.display = "none";
        }
    });

    comunaSelect.value = ""; 
}

function agregarCampoFoto() {
    const contenedor = document.getElementById("contenedor-fotos");

    const totalInputs = contenedor.querySelectorAll('input[type="file"]').length;

    if (totalInputs >= 5) {
        alert("Solo puedes subir hasta 5 fotos.");
        return;
    }

    const nuevoInput = document.createElement("input");
    nuevoInput.type = "file";
    nuevoInput.name = "foto"; 
    nuevoInput.accept = "image/*";
    contenedor.appendChild(document.createElement("br"));
    contenedor.appendChild(nuevoInput);
}

// Anti doble submit
let formularioEnviado = false;

document.querySelector('form').addEventListener('submit', function(event) {
    if (formularioEnviado) {
        event.preventDefault();
        return;
    }

    let errores = 0;

    const campos = [
        { id: 'nombre', validacion: v => v.length > 0 && v.length <= 200, mensaje: 'Nombre inválido' },
        { id: 'correo', validacion: v => /^\S+@\S+\.\S+$/.test(v) && v.length <= 100, mensaje: 'Correo inválido' },
        { id: 'sector', validacion: v => v.length <= 100 && v.length > 0, mensaje: 'Sector inválido' },
        { id: 'numero', validacion: v => /^\+569\d{8}$/.test(v), mensaje: 'Celular inválido (+569XXXXXXXX)' },
        { id: 'descripcion', validacion: v => v.length > 0, mensaje: 'Descripción obligatoria' }
    ];

    campos.forEach(campo => {
        const valor = document.getElementById(campo.id).value.trim();
        const errorDiv = document.getElementById(`error-${campo.id}`);
        if (!campo.validacion(valor)) {
            errorDiv.textContent = campo.mensaje;
            errores++;
        } else {
            errorDiv.textContent = '';
        }
    });
  });