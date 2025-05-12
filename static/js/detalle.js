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
