const express = require('express');
const app = express();
app.use(express.json());

let peers = {};

app.post('/Login', (req, res) => {
    const peerInfo = req.body;
    if (!peers[peerInfo.id]) {
        peers[peerInfo.id] = {
            ...peerInfo,
            archivos: []
        };
        res.send('Peer registrado con éxito');
    } else {
        res.status(400).send('Este peer ya está registrado.');
    }
    console.log(peerInfo);
});

app.post('/Logout', (req, res) => {
    const peerId = req.body.id;
    delete peers[peerId];
    res.send('Peer eliminado con éxito');
    console.log(`El peer ${peerId} ha sido elimnado`);
});

app.post('/indexar', (req, res) => {
    const { id, archivos } = req.body;
    if (peers[id]) {
        peers[id].archivos = archivos;
        res.send('Archivos indexados con éxito');
    } else {
        res.status(400).send('Peer no encontrado');
    }
    console.log(`Archivos del peer ${id} han sido indexados`);
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Servidor corriendo en el puerto ${PORT}`);
});