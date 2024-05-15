const express = require('express');
const axios = require('axios');

const app = express();

app.use(express.json());

// config ports
const serverPort = 9880;
const startPort = 9870;
const endPort = 9879;



// lookup table with init
let table = new Map();

async function updateNameWithPort(start, end) {
  console.log("[info] updating table...");
  // listen ports from 9870-9879
  const listeningPorts = Array.from( { length: end-start+1 }, (_, i) => i+start );

  const newTable = new Map();
  async function updateOne(port) {
    try {
      const resp = await axios.get(`http://localhost:${port}/v1/models`);
      const respData = resp.data;
      const modelNames = Array.from(respData.data, (item) => item.id );
      modelNames.forEach((mname) => { 
        newTable.set(mname, port); // FIXME: this set will cause conflictions
        console.log(`add rule: ${mname} --> ${port}`);
      });
    } catch(error) {
      console.log("no model runs on " + port);
    }
  }
  await Promise.allSettled(listeningPorts.map(updateOne));

  table = newTable;
  console.log(table);
}

// update table every 15s.
setInterval(()=>{
  updateNameWithPort(startPort, endPort)
    .catch(error => {
      console.log(`[error] server has no response from port ${serverPort}, can not update forwarding table. error info: ${error}`);
    })
},15000);


async function viewModels(validPorts) {
  const results = await Promise.all(
    validPorts.map(async (port) => {
      const resData = await axios.get(`http://localhost:${port}/v1/models`);
      return resData.data.data;
    })
  );
  return results;
}


// Forwarding server config
app.get('/v1/models', async (req, res) => {
  try {
    updateNameWithPort(startPort, endPort);
    const validPorts = Array.from(table.values());
    const validResp = await viewModels(validPorts);
    res.status(200).json({ "object": "list", "data": validResp });
  } catch (error) {
    console.error('Error fetching models:', error);
    // Handle errors gracefully, e.g., return a specific error response
    res.status(500).json({ error: 'Failed to retrieve models' });
  }
});


// forwarding chat service
function streamHandler(url, req, res) {
  axios.post(url, req.body, {responseType: 'stream'})
  .then(stream => {
    // handle if recv data
    stream.data.on('data', (chunck) => {
      // console.log(chunck.toString());
      res.write(chunck);
    });
    // handle if recv end
    stream.data.on('end', () => {
      res.end();
    });
  })
}

function normalHandler(url, req, res) {
  axios.post(url, req.body)
  .then((result) => {
    console.log(result.data);
    res.status(200).json(result.data);
  }).catch((err) => {
    console.log(err);
    res.status(404).json(err);
  });
}


app.post('/v1/chat/completions', (req, res) => {
  const reqModel = req.body.model;
  const reqPort = table.get(reqModel);
  if (reqPort === undefined) {
    const errorMsg = {
      "object": "error",
      "message": `The model \`${reqModel}\` does not exist.`,
      "type": "NotFoundError",
      "param": null,
      "code": 404
    }
    res.status(404).json(errorMsg);
  } else {
    const url = `http://localhost:${reqPort}/v1/chat/completions`;
    if (req.body.stream=true) { streamHandler(url, req, res); } 
    else { normalHandler(url, req, res); }
  }
});



// start server
app.listen(serverPort, () => {
  console.log(`app listening on port ${serverPort}`)
})
