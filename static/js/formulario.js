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

  comunaSelect.value = ""; // Reinicia selección
}

document.querySelector('form').addEventListener('submit', function(event) {
  let errores = 0;

  const campos = [
    { id: 'nombre', validacion: v => v.length > 0 && v.length <= 200, mensaje: 'Nombre inválido' },
    { id: 'correo', validacion: v => /^\S+@\S+\.\S+$/.test(v) && v.length <= 100, mensaje: 'Correo inválido' },
    { id: 'sector', validacion: v => v.length <= 100 && v.length >0 , mensaje: 'Sector inválido' },
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

  // Contactar por
  const contactarpor = document.getElementById('contactarpor').value;
  const contacto_id = document.getElementById('contacto_id').value.trim();
  const errorContacto = document.getElementById('error-contacto_id');
  if (contactarpor === 'whatsapp') {
    if (!/^\+569\d{8}$/.test(contacto_id)) {
      errorContacto.textContent = 'El identificador debe ser un número válido (+569XXXXXXXX).';
      errores++;
    } else {
      errorContacto.textContent = '';
    }
  } else {
    if (contacto_id.length < 4 || contacto_id.length > 50) {
      errorContacto.textContent = 'El identificador debe tener entre 4 y 50 caracteres.';
      errores++;
    } else {
      errorContacto.textContent = '';
    }
  }

  // Fechas
  const inicio = new Date(document.getElementById('fecha_inicio').value);
  const termino = new Date(document.getElementById('fecha_termino').value);
  const errorFechas = document.getElementById('error-fechas');
  if (isNaN(inicio) || isNaN(termino) || termino <= inicio) {
    errorFechas.textContent = 'La fecha de término debe ser posterior a la de inicio';
    errores++;
  } else {
    errorFechas.textContent = '';
  }

  // Fotos
  const fotos = document.getElementById('foto').files;
  const errorFotos = document.getElementById('error-foto');
  if (fotos.length < 1 || fotos.length > 5) {
    errorFotos.textContent = 'Debe subir entre 1 y 5 imágenes válidas';
    errores++;
  } else {
    let invalido = false;
    for (let i = 0; i < fotos.length; i++) {
      const ext = fotos[i].name.split('.').pop().toLowerCase();
      if (!['png', 'jpg', 'jpeg', 'gif'].includes(ext)) {
        invalido = true;
        break;
      }
    }
    if (invalido) {
      errorFotos.textContent = 'Archivo inválido: solo se permiten PNG, JPG, JPEG, GIF';
      errores++;
    } else {
      errorFotos.textContent = '';
    }
  }

  if (errores > 0) {
    event.preventDefault();
  }
});

