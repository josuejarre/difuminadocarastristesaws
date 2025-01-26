Codigo fuente de un trabajo realizado para emborronar las caras dependiendo si esta triste y tambien para comparar dos images e indicar si en una
de las imagenes aparece una de las personas de las fotos pasadas.
Si deseas ejecutalo, hazlo en un terminal y cuando el servidor este en espera ejecuta un curl. aqui tienes un ejemplo en linux

en este caso para comparar dos caras
curl -X POST http://127.0.0.1:5000/api/comparar -H "Content-Type: application/json" -d '{"keys": ["nombre de la primera imagen que esta en tu bucket.jpg", "nombre de la segunda imagen que esta en tu bucket.jpg"]}

En este para borrar las caras
curl -X POST http://127.0.0.1:5000/api/analyze -H "Content-Type: application/json" -d '{"key": "Nombre de la imagen que tienes en tu bucket.jpeg"}'
