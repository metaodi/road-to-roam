const RoamPrivateApi = require('roam-research-private-api');
require('dotenv').config()
var fs = require('fs');

const api = new RoamPrivateApi(process.env.ROAM_API_GRAPH,process.env.ROAM_API_EMAIL, process.env.ROAM_API_PASSWORD);

// read from stdin
var input = fs.readFileSync( 0, 'utf-8' );
var parsedInput = JSON.parse(input);

api.import(
    parsedInput
).then( () => {
    console.log( 'Import successful' );
    process.exit(0);
}).catch(error => {
    console.log("ERROR occured: ", error);
    process.exit(1);
});
