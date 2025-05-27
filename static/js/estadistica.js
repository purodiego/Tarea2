
  document.addEventListener("DOMContentLoaded", () => {
  fetch("/api/estadistica/actividades_por_dia")
    .then(res => res.json())
    .then(data => {
      const fechas = data.map(d => d.fecha);
      const cantidades = data.map(d => d.cantidad);

      const ctx = document.createElement("canvas");
      document.getElementById("grafico-lineas").appendChild(ctx);

      new Chart(ctx, {
        type: 'line',
        data: {
          labels: fechas,
          datasets: [{
            label: "Actividades por día",
            data: cantidades,
            borderColor: 'rgba(54, 162, 235, 1)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            tension: 0.4
          }]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: "Cantidad de actividades por día"
            }
          }
        }
      });
    });
});

fetch("/api/estadistica/actividades_por_tema")
  .then(res => res.json())
  .then(data => {
    const temas = data.map(d => d.tema);
    const cantidades = data.map(d => d.cantidad);

    const ctx = document.createElement("canvas");
    document.getElementById("grafico-torta").appendChild(ctx);

    new Chart(ctx, {
      type: 'pie',
      data: {
        labels: temas,
        datasets: [{
          data: cantidades,
          backgroundColor: [
            '#FF6384', '#36A2EB', '#FFCE56',
            '#4BC0C0', '#9966FF', '#FF9F40',
            '#8D6E63', '#81C784', '#BA68C8', '#F06292'
          ]
        }]
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: 'Distribución de actividades por tipo/tema'
          }
        }
      }
    });
  });

  
fetch("/api/estadistica/actividades_por_franja")
  .then(res => res.json())
  .then(data => {
    const meses = data.map(d => d.mes);
    const maniana = data.map(d => d.mañana);
    const mediodia = data.map(d => d.mediodia);
    const tarde = data.map(d => d.tarde);

    const ctx = document.createElement("canvas");
    document.getElementById("grafico-barras").appendChild(ctx);

    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: meses,
        datasets: [
          {
            label: 'Mañana',
            data: maniana,
            backgroundColor: '#42a5f5'
          },
          {
            label: 'Mediodía',
            data: mediodia,
            backgroundColor: '#66bb6a'
          },
          {
            label: 'Tarde',
            data: tarde,
            backgroundColor: '#ffa726'
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: 'Actividades por franja horaria y mes'
          }
        },
        scales: {
          x: {
            stacked: false
          },
          y: {
            beginAtZero: true
          }
        }
      }
    });
  });
