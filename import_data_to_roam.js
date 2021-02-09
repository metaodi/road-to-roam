const RoamPrivateApi = require('roam-research-private-api');
require('dotenv').config()
var fs = require('fs');

const api = new RoamPrivateApi(process.env.ROAM_API_GRAPH,process.env.ROAM_API_EMAIL, process.env.ROAM_API_PASSWORD);
let r = Math.random().toString(36).substring(7);
api.import([
    {
        title: `Test123 ${r}`,
	    children: [ { string: 'Test child' }, { string: 'Another test child', children: [{ string: "I'm a sub-element"}, {string: "Me too"}]} ] 
    },
]).then( () => {
    console.log( 'Import successful' );
    process.exit(0);
}).catch(error => {
    console.log("ERROR occured: ", error);
    process.exit(1);
});
