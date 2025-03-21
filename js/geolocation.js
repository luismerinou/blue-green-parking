function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;

            const locationElement = document.getElementById("location");

            locationElement.innerHTML = `Latitud: ${latitude}, Longitud: ${longitude}`;

            fetch("http://localhost:8000/save_location", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ latitude, longitude })
            }).then(response => response.json())
              .then(data => console.log("Respuesta del servidor:", data))
              .catch(error => console.error("Error:", error));
        }, (error) => {
            console.error("Error al obtener la ubicación:", error);
        });
    } else {
        console.error("Geolocalización no soportada por este navegador.");
    }
}
