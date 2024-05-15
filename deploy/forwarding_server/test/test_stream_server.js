// It's a test file! Not for use!
// from chaigpt
const axios = require('axios');
const express = require('express');

const url = 'http://127.0.0.1:9879/v1/chat/completions';
// const body = {
//     "model": "Qwen/Qwen1.5-1.8B-Chat-GGUF",
//     "messages": [
//         'role': 'user', 
//         'content': 'Count to 10, with a comma between each number and no newlines. E.g., 1, 2, 3, ...'
//       }
//     ],
//     "stream":true
//   }


// axios.post(url, body,  {responseType: 'stream'})
//   .then(
//     (response) => {
//       return response.data
//     }
//   )
//   .then(
//     (stream) => {
//       stream.on('data', (data) => {
//         console.log(data.toString());
//       });
//     }
//   )

const app = express();

app.use(express.json());

function streamHandler(req, res) {
  axios.post( url, req.body, {responseType: 'stream'})
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

app.post("/v1/chat/completions", streamHandler);


app.listen(9880, () => {
  console.log(`app listening on port 9880`)
});
