const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(bodyParser.text({ type: '*/*' }));

app.post('/run-lpb', (req, res) => {
    const codigoLPB = req.body;

    const tempFile = path.join(__dirname, 'temp.lpb');
    fs.writeFileSync(tempFile, codigoLPB);

    exec(`python LPB_interpretador.py ${tempFile}`, (error, stdout, stderr) => {
        fs.unlinkSync(tempFile);

        if (error) {
            console.error('Erro ao executar Python:', stderr);
            return res.status(500).send(`Erro ao executar Python:\n${stderr}`);
        }
        res.send(stdout);
    });
});

app.listen(3000, () => console.log('Servidor LPB rodando na porta 3000'));
