const express = require('express');
const axios = require('axios');

const app = express();

const serverPort = 9880;





// lookup table with init
const table = new Map();
async function updateOne(port) {
  try {
    const resp = await axios.get(`http://localhost:${port}/v1/models`);
    const respData = resp.data;
    const modelNames = Array.from(respData.data, (item) => item.id );
    modelNames.forEach((mname) => { 
      table.set(mname, port);
      console.log(`add rule: ${mname} --> ${port}`);
    });
  } catch(error) {
    console.log("no model runs on " + port);
  }
}

async function updateNameWithPort(start, end) {
  // listen ports from 9870-9879
  console.log("[info] updating table...");
  const listeningPorts = Array.from( { length: end-start+1 }, (_, i) => i+start );
  await Promise.allSettled(listeningPorts.map(updateOne));
  console.log(table);
}

updateNameWithPort(9870, 9879);




// Forwarding server config
app.get('/v1/models', (req, res) => { })
app.post('/v1/chat/completions', (req, res) => { })



// start server
app.listen(serverPort, () => {
  console.log(`app listening on port ${serverPort}`)
})
