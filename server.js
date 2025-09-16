const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(bodyParser.text({ type: '*/*' })); // aceita texto puro

// Rota principal para testes
app.get('/', (req, res) => {
  res.send('Servidor LPB rodando 🚀');
});

// Endpoint para executar LPB
app.post('/run-lpb', (req, res) => {
  const codigoLPB = req.body;

  // Criar arquivo temporário
  const tempFile = path.join(__dirname, 'temp_code.lpb');
  fs.writeFileSync(tempFile, codigoLPB);

  // Executar interpretador Python
  exec(`python3 LPB_interpretador.py ${tempFile}`, (error, stdout, stderr) => {
    if (error) {
      console.error('Erro ao executar Python:', stderr);
      return res.status(500).send(`Erro ao executar Python:\n${stderr}`);
    }

    res.send(stdout || 'Executado com sucesso, mas sem saída');
  });
});

// Porta dinâmica do Render
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Servidor LPB rodando na porta ${PORT}`);
});
