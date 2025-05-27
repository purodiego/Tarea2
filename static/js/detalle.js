const overlay = document.getElementById('overlay');
const imagenGrande = document.getElementById('imagenGrande');

document.querySelectorAll('.miniatura').forEach(img => {
  img.addEventListener('click', function(e) {
    e.stopPropagation();
    imagenGrande.src = this.src;
    overlay.style.display = 'flex';
  });
});

function cerrarImagen() {
  overlay.style.display = 'none';
}




document.addEventListener("DOMContentLoaded", () => {
  
  const form = document.getElementById("form-comentario");
  const erroresDiv = document.getElementById("errores-comentario");
  const lista = document.getElementById("lista-comentarios");

  function cargarComentarios() {
    fetch(`/api/comentarios/${actividadId}`)
      .then(res => res.json())
      .then(data => {
        lista.innerHTML = "";
        data.forEach(c => {
          const li = document.createElement("li");
          li.innerHTML = `<strong>${c.nombre}</strong>: ${c.texto}`;
          lista.appendChild(li);
        });
      });
  }

  form.addEventListener("submit", e => {
    e.preventDefault();
    erroresDiv.innerHTML = "";

    const formData = new FormData(form);

    fetch(`/api/comentarios/${actividadId}`, {
      method: "POST",
      body: formData
    })
    .then(res => {
      if (!res.ok) return res.json().then(err => Promise.reject(err));
      return res.json();
    })
    .then(() => {
      form.reset();
      cargarComentarios();
    })
    .catch(err => {
      if (err.errores) {
        for (const campo in err.errores) {
          const p = document.createElement("p");
          p.textContent = err.errores[campo];
          erroresDiv.appendChild(p);
        }
      }
    });
  });

  cargarComentarios();
});
