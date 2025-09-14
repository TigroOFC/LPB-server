const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(bodyParser.text({ type: '*/*' }));

app.post('/run-lpb', (req, res) => {
    const codigoLPB = req.body;

    // Salva temporariamente o arquivo .lpb
    const tempFile = path.join(__dirname, 'temp.lpb');
    fs.writeFileSync(tempFile, codigoLPB);

    // Usa python3 no Linux (Railway)
    exec(`python3 LPB_interpretador.py ${tempFile}`, (error, stdout, stderr) => {
        // Deleta o arquivo temporário
        fs.unlinkSync(tempFile);

        if (error) {
            console.error('Erro ao executar Python:', stderr);
            return res.status(500).send(`Erro ao executar Python:\n${stderr}`);
        }

        console.log('Saída Python:', stdout);
        res.send(stdout);
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Servidor LPB rodando na porta ${PORT}`));
