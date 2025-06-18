function enviarNota(actividadId, select) {
  const nota = parseInt(select.value);
  if (!nota || nota < 1 || nota > 7) {
    alert("La nota debe estar entre 1 y 7.");
    return;
  }

  fetch(`/api/evaluar/${actividadId}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ nota })
  })
  .then(res => res.json())
  .then(data => {
    if (data.promedio !== undefined) {
      document.getElementById(`nota-${actividadId}`).textContent = data.promedio.toFixed(1);
    }
  });
}