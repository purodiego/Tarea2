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
